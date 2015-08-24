__author__ = 'micmax93'

import struct
from collections import namedtuple
import socket
import select

# Network order - big endian
_magic_word = 0xFACE
_aim_version = 0x01

_header_fmt = struct.Struct('!Hbbb')


def make_header(msg_type, payload_size):
    return _header_fmt.pack(_magic_word, _aim_version, msg_type, payload_size)


def read_header(raw_data):
    data = _header_fmt.unpack(raw_data)
    return data[2], data[3]

# Commands
_apiGetAudienceStatus = 0
_apiGetAudienceDetails = 1
_apiGetViewerEvents = 5

# Events
_EVENT_ACK = 128
_EVENT_NACK = 129
_EVENT_AUDIENCE_STATUS = 130
_EVENT_AUDIENCE_DETAILS = 131
_EVENT_MAJORITY_GENDER = 132
_EVENT_VIEWER = 135

_viewer_fmt = struct.Struct('!IbbbbIHHHH')
ViewerDetail = namedtuple('ViewerDetail',
                          ['viewer_id', 'gender', 'age', 'reserved1', 'reserved2', 'viewing_time', 'x_pos', 'y_pos',
                           'width', 'height'])

_gender_unknown = 0
_gender_male = 1
_gender_female = 2

_age_unknown = 0
_age_child = 1
_age_teen = 2
_age_young = 3
_age_older = 4
_age_senior = 5


class InvalidResponseException(Exception):
    pass


class CommandFailedException(Exception):
    pass


def get_viewer_detail(data):
    return ViewerDetail._make(_viewer_fmt.unpack(data))


class ApiConnection(object):
    def __init__(self, host='127.0.0.1', port=12500):
        self.conn = socket.create_connection(address=(host, port))

    def _get_response_header(self):
        raw_data = self.conn.recv(5)
        return read_header(raw_data)

    def _get_response(self):
        msg, load = self._get_response_header()
        if load == 0:
            return msg, None
        data = self.conn.recv(load)
        return msg, data

    def get_audience_status(self):
        self.conn.sendall(make_header(_apiGetAudienceStatus, 0))
        msg, data = self._get_response()
        if msg == _EVENT_NACK:
            raise CommandFailedException()
        elif msg == _EVENT_AUDIENCE_STATUS:
            return struct.unpack('!B', data)[0]
        else:
            raise InvalidResponseException(msg)

    def get_audience_details(self):
        self.conn.sendall(make_header(_apiGetAudienceDetails, 0))
        msg, load = self._get_response_header()
        if msg == _EVENT_NACK:
            raise CommandFailedException()
        elif msg == _EVENT_AUDIENCE_DETAILS:
            n = struct.unpack('!B', self.conn.recv(1))[0]
            viewers = []
            for i in range(n):
                viewer = get_viewer_detail(self.conn.recv(20))
                viewers.append(viewer)
            return viewers
        else:
            raise InvalidResponseException(msg)

    def subscribe_viewer_events(self, subscribe=True):
        self.conn.sendall(make_header(_apiGetViewerEvents, 1))
        if subscribe:
            data = struct.pack('!b', 1)
        else:
            data = struct.pack('!b', 0)
        self.conn.sendall(data)
        msg, data = self._get_response()
        if msg == _EVENT_ACK:
            return
        elif msg == _EVENT_NACK:
            raise CommandFailedException()
        else:
            raise InvalidResponseException(msg)

    def receive_viewer_event(self):
        msg, load = self._get_response_header()
        if msg != _EVENT_VIEWER:
            raise InvalidResponseException(msg)
        e_type = struct.unpack('!B', self.conn.recv(1))
        viewer = get_viewer_detail(self.conn.recv(20))
        return (e_type == 0), viewer
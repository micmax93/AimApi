import time
from datetime import datetime

__author__ = 'micmax93'
from api import ApiConnection
from player import SinglePlayer
from loader import load_configs
from grid import PublishersList, ViewersGrid
from ConfigParser import ConfigParser
from logger import CsvLogger


_config = ConfigParser()
_config.read('config.ini')
_path = _config.get('global', 'path')
_mode = _config.getboolean('global', 'targeted')


publishers, _grid = load_configs(_path)
pub_list = PublishersList(_grid)

player = SinglePlayer()

api = ApiConnection(host='25.152.172.38')
log = CsvLogger('log.csv', ['date', 'video', 'viewers', 'value'])


def get_viewers_grid(viewers):
    grid = ViewersGrid()
    for viewer in viewers:
        grid.add(viewer.age, viewer.gender)
    return grid

_gender_dict = ['unknown', 'male', 'female']
_age_dict = ['unknown', 'child', 'teen', 'young', 'older', 'senior']


def run_once():
    audience = api.get_audience_details()
    viewers_grid = get_viewers_grid(audience)
    pub = pub_list.select_publisher(viewers_grid, targeted_alg=_mode)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    player.set_next(publishers[pub]['video'])
    log.write_row([now, publishers[pub]['video'], len(audience), pub_list.publishers[pub]['viewers']])
    for a in audience:
        publishers[pub]['log'].write_row([now, a.viewer_id, _age_dict[a.age], _gender_dict[a.gender]])
    time.sleep(3)
    player.wait(margin=900)


if __name__ == '__main__':
    while True:
        run_once()
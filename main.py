__author__ = 'micmax93'
from api import ApiConnection
from player import SinglePlayer
from loader import load_configs
from grid import SubscribersList, ViewersGrid
from ConfigParser import ConfigParser


_config = ConfigParser()
_config.read('config.ini')
_path = _config.get('global', 'path')
_mode = _config.getboolean('global', 'targeted')


subscribers, _grid = load_configs(_path)
sub_list = SubscribersList(_grid)

player = SinglePlayer()

api = ApiConnection(host='25.152.172.38')


def get_viewers_grid(viewers):
    grid = ViewersGrid()
    for viewer in viewers:
        grid.add(viewer.age, viewer.gender)
    return grid


def run_once():
    audience = api.get_audience_details()
    viewers_grid = get_viewers_grid(audience)
    sub = sub_list.select_subscriber(viewers_grid, targeted_alg=_mode)
    player.set_next(subscribers[sub]['video'])
    player.wait()


if __name__ == '__main__':
    while True:
        run_once()
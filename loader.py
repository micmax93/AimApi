__author__ = 'micmax93'

from ConfigParser import ConfigParser
import os
import re
import logger
from grid import SubscribersGrid


def get_config_files(path):
    configs = {}
    for root, directories, filenames in os.walk(path):
        for f in filenames:
            mo = re.match('^(.+)\.ini$', f)
            if mo is not None:
                cp = ConfigParser()
                cp.read(os.path.join(root, f))
                f_name = os.path.join(root, mo.group(1))
                configs[f_name] = {'ini': cp, 'path': root}
    return configs


def build_grid(configs):
    grid = SubscribersGrid()
    for key in configs:
        viewers = configs[key]['ini'].items('viewers')
        for age, gender in viewers:
            grid.add(age, gender, key)
    return grid


def check_videos(configs):
    for key in configs:
        configs[key]['log'] = logger.CsvLogger(key + '.csv', ['date', 'id', 'age', 'gender'])
        configs[key]['video'] = key + '.' + configs[key]['ini'].get('video', 'extension')
        assert os.path.isfile(configs[key]['video']), configs[key]['video'] + ' does not exists.'
    return configs


def load_configs(path):
    configs = get_config_files(path)
    configs = check_videos(configs)
    grid = build_grid(configs)
    return configs, grid
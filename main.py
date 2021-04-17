import core.run.task as task
import json
from core.conf.config import config as configuration
import configparser

# python 3.8


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('./config.ini')
    configuration.load(dbc=config['dbc'], storage=config['storage'])
    configuration.start()


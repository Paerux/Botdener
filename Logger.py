import logging.config
import yaml


def setup():
    with open('config/log_config.yml', 'r') as stream:
        config = yaml.safe_load(stream)
    logging.config.dictConfig(config)

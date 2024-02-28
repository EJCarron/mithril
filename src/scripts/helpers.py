import json
import sys
from . import config
import click


def check_and_init_config():
    try:
        with open("config.json", "r") as f:
            config_dict = json.load(f)
    except():
        click.echo("config json file doesn't exist. Use \'chi set_config\' command")
        sys.exit()

    if config_dict is None or len(config_dict) == 0 :
        click.echo('set config.')
        sys.exit()

    return config.Config(**config_dict)

def set_config(**kwargs):
    try:
        with open("config.json", "r") as f:
            config_dict = json.load(f)
    except:
        config_dict = {}

    for key, value in kwargs.items():
        config_dict[key] = value

    try:
        with open("config.json", "w") as f:
            json.dump(config_dict, f)
    except Exception as e:
        click.echo('failed to write config file.')
        click.echo(e)


def get_config():
    return check_and_init_config()

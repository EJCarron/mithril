from ..objects.network import Network
from . import helpers
import click
from . import save_network
import sys


def setconfig(**kwargs):

    helpers.set_config(**kwargs)


def createnetwork(ch_officer_ids=None, ch_company_numbers=None, save_json_path='',
                  save_csvs_path='',
                  save_xlsx_path='', save_neo4j='', overwrite_neo4j=False):
    config = helpers.check_and_init_config()

    ch_officer_ids = [] if ch_officer_ids is None else ch_officer_ids
    ch_company_numbers = [] if ch_company_numbers is None else ch_company_numbers

    network = Network.start(ch_officer_ids=ch_officer_ids, ch_company_numbers=ch_company_numbers)

    if save_json_path != "":
        try:
            save_network.save_json(network=network, path=save_json_path)
        except Exception as e:
            click.echo("failed to save json")
            click.echo(e)

    if save_csvs_path != "":
        try:
            save_network.save_csvs(network=network, path=save_csvs_path)
        except Exception as e:
            click.echo("failed to save csvs. REMINDER to save csvs provide path to existing directory not to a .csv "
                       "file")
            click.echo(e)

    if save_xlsx_path != "":
        try:
            save_network.save_xlsx(network=network, path=save_xlsx_path)
        except Exception as e:
            click.echo("failed to save xlsx")
            click.echo(e)

    if save_neo4j:
        try:
            save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j)
        except Exception as e:
            click.echo("Failed to save neo4j graph db")
            click.echo(e)

    return network


def load_network(load_path):
    try:
        network = Network.load_json(load_path)
    except Exception as e:
        click.echo('Failed to load network')
        click.echo(e)
        sys.exit()

    return network


def loadjsoncreategraph(load_path, overwrite_neo4j):
    config = helpers.check_and_init_config()

    network = load_network(load_path)

    save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j)


def loadjsonsavecsvs(load_path, save_path):
    network = load_network(load_path)

    try:
        save_network.save_csvs(network=network, path=save_path)
    except Exception as e:
        click.echo("failed to save csvs. REMINDER to save csvs provide path to existing directory not to a .csv "
                   "file")
        click.echo(e)


def loadjsonsavexlsx(load_path, save_path):
    network = load_network(load_path)

    try:
        save_network.save_xlsx(network=network, path=save_path)
    except Exception as e:
        click.echo("failed to save xlsx")
        click.echo(e)
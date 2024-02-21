from ..objects.network import Network
from . import helpers
import click
from . import save_network


def setconfig(normal_key, uri, username, pw):
    config_dict = {'normal_key': normal_key,
                   'uri': uri,
                   'username': username,
                   'pw': pw
                   }

    helpers.set_config(config_dict)


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

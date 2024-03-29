from ..objects.network import Network
from . import helpers
import click
from . import save_network
import sys
from .cross_referencing import cross_referencing


def setconfig(**kwargs):
    helpers.set_config(**kwargs)


def create_same_as_relationships(relationships, network):
    for relationship in relationships:
        # could input kwargs but leaving this here to remind that relationships needs to be list
        # of dicts with these keys
        network.create_same_as_relationship(parent_node_id=relationship['parent_node_id'],
                                            child_node_id=relationship['child_node_id']
                                            )

    return network


def createnetwork(ch_officer_ids=None, ch_company_numbers=None, ol_node_ids=None,
                  save_json_path='',
                  save_csvs_path='',
                  save_xlsx_path='', save_neo4j='', overwrite_neo4j=False, same_as=None):
    config = helpers.check_and_init_config()

    ch_officer_ids = [] if ch_officer_ids is None else ch_officer_ids
    ch_company_numbers = [] if ch_company_numbers is None else ch_company_numbers
    ol_node_ids = [] if ol_node_ids is None else ol_node_ids
    same_as = [] if same_as is None else same_as

    network = Network.start(ch_officer_ids=ch_officer_ids, ch_company_numbers=ch_company_numbers,
                            offshore_leaks_node_ids=ol_node_ids)

    create_same_as_relationships(same_as, network)

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


def find_potential_offshore_leaks_matches(json_path):
    network = load_network(json_path)

    potential_matches = cross_referencing.find_potential_connections_in_offshore_leaks_db(network)

    return potential_matches


def add_offshore_leak_connections_to_network(json_path, matches):
    network = load_network(json_path)

    network = cross_referencing.add_offshore_leaks_connections_to_network(matches=matches, network=network)

    network.save_json(json_path)

def find_potential_donations_matches(json_path):
    network = load_network(json_path)
    return cross_referencing.find_potential_donations_matches(network)

def add_donations_connections_to_network(json_path, matches):
    network = load_network(json_path)

    network = cross_referencing.add_donations_connections_to_network(matches=matches, network=network)

    network.save_json(json_path)

from src.objects.network import Network
from src.scripts import helpers
import click
from src.scripts import save_network
import sys
from src.scripts.cross_referencing import cross_referencing
from src.scripts.companies_house import companies_house_api
from src.scripts.timeline import timeline as tl
from src.objects.graph_objects.nodes import node_factory
from src.scripts.uk_electoral_commission import electoral_commission_api
from src.scripts.OffshoreLeaks import offshore_leaks_api


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


def make_network_from_dict(network_dict):
    return Network.from_dict(network_dict)


def expand_network(network, target_node_ids=None):
    network.expand(target_node_ids)
    return network


def make_same_as_connections(network, node_ids):
    if len(node_ids) <= 1:
        return None

    first_node_id = node_ids[0]

    for i in range(len(node_ids)):
        if i == 0:
            continue

        network.create_same_as_relationship(first_node_id=first_node_id, second_node_id=node_ids[i])

    return network


def companies_house_search(query, page_number, search_type=None):
    if search_type is None:
        return companies_house_api.search_all(query, page_number)
    elif search_type == 'company':
        return companies_house_api.search_companies(query, page_number)
    elif search_type == 'officer':
        return companies_house_api.search_officers(query, page_number)
    else:
        print(f'invalid search type {search_type}')
        return None


def node_search(query, page_number, search_type):
    if search_type == 'Companies House All' or search_type in \
            [node_factory.ch_company_str, node_factory.ch_officer_str]:
        search_type = None if search_type == 'Companies House All' else search_type
        return companies_house_api.companies_house_search(query, page_number, search_type)
    elif search_type == 'Electoral Commission All' or search_type in node_factory.ec_nodes_dict.keys():
        search_type = None if search_type == 'Electoral Commission All' else search_type
        return electoral_commission_api.search_typesense(query, page_number, search_type)
    elif search_type == 'Offshore Leaks All' or search_type in node_factory.ol_keys_dict.keys():
        search_type = None if search_type == 'Offshore Leaks All' else search_type
        return offshore_leaks_api.search_typesense(query, page_number, search_type)


def export_timeline(network, export_path):
    timeline = tl.make_timeline(network)
    tl.export_time_line_to_xlsx(timeline, export_path)


def createnetwork(core_nodes,
                  save_csvs_path='',
                  save_xlsx_path='', save_neo4j=False, overwrite_neo4j=False, same_as=None, expand=0, network_name=''):
    config = helpers.check_and_init_config()

    same_as = [] if same_as is None else same_as

    network = Network.start(core_nodes, network_name=network_name)

    create_same_as_relationships(same_as, network)

    if expand > 0:
        for i in range(expand):
            network.expand()

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
        print('saving as Neo4j graph db')
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


def exportcsvs(network, export_path):
    try:
        save_network.save_csvs(network=network, path=export_path)
    except Exception as e:
        click.echo("failed to save csvs. REMINDER to save csvs provide path to existing directory not to a .csv "
                   "file")
        click.echo(e)


def exportxlsx(network, export_path):
    try:
        save_network.save_xlsx(network=network, path=export_path)
    except Exception as e:
        click.echo("failed to save xlsx")
        click.echo(e)


def exportgraph(network, overwrite_neo4j):
    config = helpers.check_and_init_config()
    save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j)


def loadjsoncreategraph(load_path, overwrite_neo4j):
    network = load_network(load_path)

    exportgraph(network, overwrite_neo4j)


def loadjsonsavecsvs(load_path, save_path):
    network = load_network(load_path)

    exportcsvs(network, save_path)


def loadjsonsavexlsx(load_path, save_path):
    network = load_network(load_path)

    exportcsvs(network, save_path)


def find_potential_offshore_leaks_matches(network):
    potential_matches = cross_referencing.find_potential_connections_in_offshore_leaks_db(network)

    return potential_matches


def add_offshore_leak_connections_to_network(network, matches):
    network = cross_referencing.add_offshore_leaks_connections_to_network(matches=matches, network=network)

    return network


def find_potential_electoral_commission_donation_matches(network, drop_tokens_threshold):
    return cross_referencing.find_potential_electoral_commission_donation_matches(network, drop_tokens_threshold)


def add_electoral_commission_donation_connections_to_network(network, matches):
    network = cross_referencing.add_electoral_commission_donation_connections_to_network(matches=matches,
                                                                                         network=network)

    return network


def add_nodes_to_network(network, add_nodes):
    network.add_nodes(add_nodes)
    return network
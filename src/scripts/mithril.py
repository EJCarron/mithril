import click
from . import mithril_functions


@click.group()
def mithril():
    pass


@mithril.command()
@click.option("--normal_key", "-nk", prompt='Your Companies House api Key',
              help="You need to make an account with Companies House to have a key.", default='')
@click.option("--uri", "-uri", prompt='Your neo4j DB uri', default='')
@click.option("--username", "-un", prompt="Your neo4j username", default='neo4j')
@click.option("--pw", "-pw", prompt="Your neo4j db password", default='')
@click.option("--appointment_limit", "-al", default=100)
@click.option("--offshore_leaks_db_path", "-oldp", default='')
def setconfig(normal_key, uri, username, pw, appointment_limit, offshore_leaks_db_path):
    mithril_functions.setconfig(normal_key=normal_key, uri=uri, username=username, pw=pw,
                                appointment_limit=appointment_limit, offshore_leaks_db_path=offshore_leaks_db_path)


@mithril.command()
@click.option("--ch_officer_ids", "-choid", multiple=True, default=[], required=False,
              help="Can be found in the url of the person\'s Companies House profile.")
@click.option("--ch_company_numbers", "-chcn", multiple=True, default=[], required=False,
              help="Can be found in the url of the company\'s Companies House profile.")
@click.option("--save_json_path", "-sjp", default="",
              help="Path to the json save location, will not save if left blank")
@click.option("--save_csvs_path", "-scp", default="", help="Path to the directory where you want to save your csvs,"
                                                           "directory must already exist. Will not save if left blank")
@click.option("--save_xlsx_path", "-sxp", default="",
              help="Path to the xlsx save location, will not save if left blank")
@click.option("--save_neo4j", "-sgdb", default=True, help="Bool for for whether to save the network as a graph DB."
                                                          "Defaults to True.")
@click.option("--overwrite_neo4j", "-own", default=False, help="Bool, set to True if you want to clear graph db "
                                                               "contents before writing new network")
def createnetwork(ch_officer_ids, ch_company_numbers, save_json_path, save_csvs_path,
                  save_xlsx_path, save_neo4j, overwrite_neo4j):
    mithril_functions.createnetwork(ch_officer_ids=ch_officer_ids, ch_company_numbers=ch_company_numbers,
                                    save_json_path=save_json_path,
                                    save_csvs_path=save_csvs_path, save_xlsx_path=save_xlsx_path, save_neo4j=save_neo4j,
                                    overwrite_neo4j=overwrite_neo4j)


@mithril.command()
@click.option("--load_path", "-lp", prompt="path to the save location.")
def loadjsoncreategraph(load_path, overwrite_neo4j):
    mithril_functions.loadjsoncreategraph(load_path=load_path, overwrite_neo4j=overwrite_neo4j)


@mithril.command()
@click.option("--save_path", "-sp", prompt="path to the save location.")
@click.option("--load_path", "-lp", prompt="path to the saved json location.")
def loadjsonsavecsvs(load_path, save_path):
    mithril_functions.loadjsonsavecsvs(load_path=load_path, save_path=save_path)


@mithril.command()
@click.option("--save_path", "-sp", prompt="path to the save location.")
@click.option("--load_path", "-lp", prompt="path to the saved json location.")
def loadjsonsavexlsx(load_path, save_path):
    mithril_functions.loadjsonsavexlsx(load_path=load_path, save_path=save_path)

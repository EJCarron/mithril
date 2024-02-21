import click
from . import mithril_functions


@click.group()
def mithril():
    pass


@mithril.command()
@click.option("--ch_officer_ids", "-choid", multiple=True, default=[], required=False,
              help="Can be found in the url of the person\'s Companies House profile.")
@click.option("--ch_company_numbers", "-chcn", multiple=True, default=[], required=False,
              help="Can be found in the url of the company\'s Companies House profile.")
def createnetwork(ch_officer_ids, ch_company_numbers):
    mithril_functions.createnetwork(ch_officer_ids=ch_officer_ids, ch_company_numbers=ch_company_numbers)
    

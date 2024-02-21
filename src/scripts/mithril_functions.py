from ..objects.network import Network
from . import helpers


def setconfig(normal_key, uri, username, pw):
    config_dict = {'normal_key': normal_key,
                   'uri': uri,
                   'username': username,
                   'pw': pw
                   }

    helpers.set_config(config_dict)


def createnetwork(ch_officer_ids=None, ch_company_numbers=None):
    ch_officer_ids = [] if ch_officer_ids is None else ch_officer_ids
    ch_company_numbers = [] if ch_company_numbers is None else ch_company_numbers

    network = Network.start(ch_officer_ids=ch_officer_ids, ch_company_numbers=ch_company_numbers)

    return network

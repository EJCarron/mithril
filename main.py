from src.scripts import mithril_functions



# configs = {'fuzzy_officer_table': 'officers_fuzzy',
#               'fuzzy_address_table': 'addresses_fuzzy',
#               'fuzzy_intermediary_table': 'intermediaries_fuzzy',
#               'fuzzy_other_table': 'others_fuzzy',
#               'fuzzy_current_table': 'entities_current_fuzzy',
# 'fuzzy_former_table': 'entities_former_fuzzy',
#            'fuzzy_officer_threshold': 3,
#                   'fuzzy_address_threshold': 3,
#                   'fuzzy_intermediary_threshold': 3,
#                   'fuzzy_other_threshold': 3,
#                   'fuzzy_entity_threshold': 3
#                   }

path = '/Users/edwardcarron/Desktop/chi_test/ashcroft_network.json'

# network = mithril_functions.createnetwork(ch_officer_ids=['xt5GXEWn29VeX2Lv5RfI0-HMyz0'], save_json_path=path)
mithril_functions.find_potential_offshore_leaks_matches(path)



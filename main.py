from src.scripts import mithril_functions
import json


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
# matches = mithril_functions.find_potential_offshore_leaks_matches(path)

# good = ['2582909', '258068', '372562']
# good_matches = []
# for match in matches:
#     if match['values']['id'] in good:
#         good_matches.append(match)

        # print('{name} | {match_name}, {typesense_id}'.format(name=match['name'], match_name=match['matched_to'],
        #                                                typesense_id=match['id']))

# mithril_functions.add_offshore_leak_connections_to_network(path, good_matches)

mithril_functions.loadjsoncreategraph(path, True)



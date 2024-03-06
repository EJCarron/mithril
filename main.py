import mithril
from src.scripts.uk_electoral_commission.populate_db import populate_db

populate_db()


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

# path = '/Users/edwardcarron/Desktop/chi_test/climate_network.json'
#
# network = mithril.createnetwork(ch_officer_ids=['xt5GXEWn29VeX2Lv5RfI0-HMyz0'],ol_node_ids=['80031186'],
#                                           save_neo4j=True, overwrite_neo4j=True, expand=1)
#

# path = '/Users/edwardcarron/Desktop/chi_test/ashcroft_network.json'
#
#
# mithril.loadjsoncreategraph(path, True)

# matches = mithril.find_potential_offshore_leaks_matches(path)





#
# good = ['2023', '358', '357', '356', '355', '354']
# good_matches = []
# for match in matches:
#     if match['values']['id'] in good:
#         good_matches.append(match)
#
#
#
# # for match in matches:
# #     print('{name} | {match_name}, {typesense_id}'.format(name=match['values']['Donor'], match_name=match['info']['matched_to'],
# #                                                    typesense_id=match['values']['id']))
#
#
# mithril_functions.add_donations_connections_to_network(path, good_matches)
#
#
# mithril_functions.loadjsoncreategraph(path, True)


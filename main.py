from src.scripts.data_wrangling import populate_db
from src.scripts.typesense_client import db_report, drop_collection


# db_report()

populate_db.full_populate_sequence()


# update_sequence()


# net = mithril.load_network('/Users/edwardcarron/code/ceramite/data/ashcroft.json')
# net
#
# timeline = tl.make_timeline(net)
# tl.export_time_line_to_xlsx(timeline, '/Users/edwardcarron/Desktop/chi_test/timeline.xlsx')



# db_report()

# gwpf_network = mithril.load_network('/Users/edwardcarron/Desktop/chi_test/gwpf.json')

# gwpf_network.expand_network()
#
# n_j = gwpf_network.to_json()
#
# with open('/Users/edwardcarron/Desktop/chi_test/gwpf.json', 'w') as w:
#     w.write(n_j)

# hand_matched_network = mithril.load_network('/Users/edwardcarron/code/ceramite/data/gwpf.json')
#
# same_as_relationships = hand_matched_network.get_same_as_relationships()
#
# # zero_drops_matches = mithril.find_potential_electoral_commission_donation_matches(gwpf_network, 0)
# None_drops_matches = mithril.find_potential_electoral_commission_donation_matches(gwpf_network, None)
#
#
# def sort_func(e):
#     return e['info']['match_info']['score']
#
#
# None_drops_matches.sort(key=sort_func, reverse=True)
#
#
# hand_picked_matches = []
# rejected_matches = []
#
# example = []
#
# for match in None_drops_matches:
#     hand_picked = False
#     for same_as in same_as_relationships:
#         if match['info']['compare_node_id'] == same_as.parent_id and match['values']['node_id'] == same_as.child_id:
#             hand_picked_matches.append(match)
#             hand_picked = True
#             match['picked'] = True
#             break
#
#     if not hand_picked:
#         match['picked'] = False
#
#     example.append({'query_str': match['info']['matched_to'], 'matched_str':match['values']['name'],
#                     'True Match':match['picked']})
#
#
# no_hit_counter = 0
#
# for match in example:
#     if match['True Match']:
#         if no_hit_counter > 0:
#             print(f'{no_hit_counter} misses in a row')
#             no_hit_counter = 0
#         print('HIT')
#         pprint.pprint(match)
#     else:
#         no_hit_counter +=1
#
# print(f'ends with {no_hit_counter} misses in a row')
#
#
# # pprint.pprint(example)
#
# None_drops_matches
#
#
#
#
#
#
#
#
#
#
#
# def analise_matches(matches):
#     stats = {
#         '1_token_matched': 0,
#         '0_token_matched': 0,
#         '2_token_matched': 0,
#         '3_token_matched': 0,
#         'more_token_matched': 0,
#         'min_score': None,
#         'max_score': 0,
#         'avg_score': 0,
#     }
#
#     total_score = 0
#
#     for match in matches:
#         match_info = match['info']['match_info']
#         # match_info['score'] = int(match_info['score'])
#
#         if match_info['tokens_matched'] == 0:
#             stats['0_token_matched'] += 1
#         elif match_info['tokens_matched'] == 1:
#             stats['1_token_matched'] += 1
#         elif match_info['tokens_matched'] == 2:
#             stats['2_token_matched'] += 1
#         elif match_info['tokens_matched'] == 3:
#             stats['3_token_matched'] += 1
#         else:
#             stats['more_token_matched'] += 1
#
#         if stats['min_score'] is None:
#             stats['min_score'] = match_info['score']
#         elif match_info['score'] < stats['min_score']:
#             stats['min_score'] = match_info['score']
#
#         if match_info['score'] > stats['max_score']:
#             stats['max_score'] = match_info['score']
#
#         total_score += match_info['score']
#
#     stats['avg_score'] = int(total_score / len(matches))
#
#     return stats
#
#
# hand_picked_stats = analise_matches(hand_picked_matches)
# rejected_matches = analise_matches(rejected_matches)
#
# gwpf_network
#
#





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


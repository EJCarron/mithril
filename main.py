import src.scripts.mithril_functions as mf
import src.scripts.OffshoreLeaks.offshore_leaks_api as api
from src.scripts import helpers

mf.createnetwork(ch_officer_ids=['xt5GXEWn29VeX2Lv5RfI0-HMyz0'],ol_node_ids=[80031186],
                 save_neo4j=True, overwrite_neo4j=True, same_as=[{'parent_node_id': 'xt5GXEWn29VeX2Lv5RfI0-HMyz0',
                                                                  'child_node_id': 'ol_80031186'
                                                                  }])



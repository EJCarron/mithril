import src.scripts.mithril_functions as mf
import src.scripts.OffshoreLeaks.offshore_leaks_api as api
from src.scripts import helpers

mf.createnetwork(ol_node_ids=[24000001, 10000001, 11000001, 12000001, 85004929], save_neo4j=True, overwrite_neo4j=True)



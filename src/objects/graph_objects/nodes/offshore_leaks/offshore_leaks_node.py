from ..node import Node
from .....scripts.OffshoreLeaks import offshore_leaks_api


class OffshoreLeaksNode(Node):

    def __init__(self, **kwargs):
        super(OffshoreLeaksNode, self).__init__()
        self.node_id = 'ol_' + kwargs['db_node_id']
        self.__dict__.update(kwargs)





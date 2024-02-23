from ..node import Node
from .....scripts.OffshoreLeaks import offshore_leaks_api


class OffshoreLeaksNode(Node):

    def __init__(self, **kwargs):
        super(OffshoreLeaksNode, self).__init__()
        self.db_node_id = ''
        self.__dict__.update(kwargs)

    @property
    def node_id(self):
        return "ol_" + str(self.db_node_id)




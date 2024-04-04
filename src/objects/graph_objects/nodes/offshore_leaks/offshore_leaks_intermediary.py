from .offshore_leaks_node import OffshoreLeaksNode
from .....scripts.OffshoreLeaks import offshore_leaks_api

class OffshoreLeaksIntermediary(OffshoreLeaksNode):


    @property
    def events(self):
        return []


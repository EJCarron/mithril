from .offshore_leaks_node import OffshoreLeaksNode
from .....scripts.OffshoreLeaks import offshore_leaks_api

class OffshoreLeaksOfficer(OffshoreLeaksNode):

    @property
    def events(self):
        return []
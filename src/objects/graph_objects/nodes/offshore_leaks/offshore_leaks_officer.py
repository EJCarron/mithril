from .offshore_leaks_node import OffshoreLeaksNode
from .....scripts.OffshoreLeaks import offshore_leaks_api

class OffshoreLeaksOfficer(OffshoreLeaksNode):
    def render_unique_label(self):
        start_label = self.name.replace(' ', '_')

        return start_label + str(self.db_node_id)

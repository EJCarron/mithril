from .offshore_leaks_node import OffshoreLeaksNode


class OffshoreLeaksAddress(OffshoreLeaksNode):

    def render_unique_label(self):

        start_label = self.address if self.address is not None else self.name
        if start_label is None:
            start_label = ''

        start_label = start_label.replace(' ', '_')

        return start_label + str(self.node_id)

    @property
    def events(self):
        return []


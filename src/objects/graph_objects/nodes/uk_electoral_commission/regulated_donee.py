from ..node import Node

class RegulatedDonee(Node):
    def __init__(self, **kwargs):
        super(RegulatedDonee, self).__init__()
        self.name = kwargs['name']
        self.node_id = kwargs['name'] + '_regulated_donee'
        self.__dict__.update(kwargs)

    def render_unique_label(self):
        return self.name.replace(' ', '_')
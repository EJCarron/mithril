from .node import Node
from src.scripts.generate_node_id import generate_node_id


class SameAsCentre(Node):

    def __init__(self, **kwargs):
        super(SameAsCentre, self).__init__()

        self.name = None

        self.__dict__.update(kwargs)

        self.node_id = generate_node_id(self.name, SameAsCentre.__name__)

    def render_unique_label(self):
        name = self.name.replace(' ', '_')
        return f'{name}_{self.node_id}'

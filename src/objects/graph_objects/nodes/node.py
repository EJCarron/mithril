from src.objects.graph_objects.graph_object import GraphObject


class Node(GraphObject):
    def __init__(self):
        self.node_type = type(self).__name__
        self.expanded = False

    @property
    def unique_label(self):
        node_name = self.render_unique_label()

        node_name = self.clean_name(node_name)

        return node_name

    @property
    def node_id(self):
        return 'need to implement node_id property'


    def render_unique_label(self):
        return 'need to implement render unique label'

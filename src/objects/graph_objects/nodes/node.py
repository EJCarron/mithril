from src.objects.graph_objects.graph_object import GraphObject


class Node(GraphObject):
    def __init__(self):
        self.node_type = type(self).__name__
        self.expanded = False
        self.node_id = 'not_implemented_node_id'
        self.name = 'not implemented name'

    @property
    def unique_label(self):
        node_name = self.render_unique_label()

        node_name = self.clean_name(node_name)

        return node_name

    def render_unique_label(self):
        return 'need to implement render unique label'

    def render_create_clause(self):
        parameters_string = self.render_parameters_string()

        clause_string = '''
        ({name}:{label} {{{parameters}}})
        '''.format(name=self.unique_label, label=self.node_type, parameters=parameters_string)

        return clause_string

    def expand(self):
        print('expand not implemented')
        return None
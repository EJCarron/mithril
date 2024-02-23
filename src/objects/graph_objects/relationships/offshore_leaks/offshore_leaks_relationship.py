from ..relationship import Relationship


class OffshoreLeaksRelationship(Relationship):
    def render_create_clause(self):
        parameters_string = self.render_parameters_string()

        clause = '''
        CREATE ({parent})-[: {relationship} {{{parameters}}}]->({child})
        '''.format(parent=self.clean_name(self.parent_node_name), child=self.clean_name(self.child_node_name),
                   relationship=self.rel_type,
                   parameters=parameters_string)
        return clause

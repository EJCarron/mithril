from .relationship import Relationship
from src.objects.graph_objects.nodes import node_factory


class SameAs(Relationship):
    @classmethod
    def create(cls, same_as_centre, node):
        if not isinstance(same_as_centre, node_factory.same_as_centre):
            print('SYSTEM ERROR not same as centre node')
            return None

        return cls(parent_node_name=node.unique_label, parent_id=node.node_id,
                   child_node_name=same_as_centre.unique_label, child_id=same_as_centre.node_id)


    @property
    def centre_node_id(self):
        return self.child_id


    def change_centre(self, new_centre):
        if not isinstance(new_centre, node_factory.same_as_centre):
            print('SYSTEM ERROR not same as centre node')
            return None

        self.child_id = new_centre.node_id
        self.child_node_name = new_centre.unique_label

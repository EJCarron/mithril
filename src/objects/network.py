import json
import sys
from .graph_objects.nodes import node_factory
from .graph_objects.relationships import relationship_factory
from .graph_objects import expand


class Network:
    clear_network_strings = ('match (a) -[r] -> () delete a, r', 'match (a) delete a',)

    def __init__(self, nodes=None, relationships=None):
        self.nodes = {} if nodes is None else nodes
        self.relationships = [] if relationships is None else relationships

    # Getters

    def get_nodes_of_type(self, node_type):

        found_nodes = {}

        for node_id, node in self.nodes.items():
            if isinstance(node, node_type):
                found_nodes[node_id] = node

        return found_nodes

    def get_relationships_of_type(self, relationship_type):
        found_relationships = []

        for relationship in self.relationships:
            if isinstance(relationship, relationship_type):
                found_relationships.append(relationship)

        return found_relationships

    def get_node(self, node_id):
        if node_id in self.nodes.keys():
            return self.nodes[node_id]
        else:
            print("Internal ERROR {0} node not in network".format(node_id))
            return None

    @property
    def ch_officers(self):
        return self.get_nodes_of_type(node_type=node_factory.ch_officer)

    @property
    def ch_companies(self):
        return self.get_nodes_of_type(node_type=node_factory.ch_company)

    @property
    def ch_appointments(self):
        return self.get_relationships_of_type(relationship_type=relationship_factory.ch_appointment)

    # Setters

    def set_nodes(self, new_nodes_dict):

        self.nodes = {}

        for node_id, node in new_nodes_dict.items():
            if isinstance(node, node_factory.node):
                self.nodes[node_id] = node
            else:
                print("SYSTEM ERROR non node in dict of nodes to be set")

    def set_relationships(self, new_relationships):

        self.relationships = []

        for relationship in new_relationships:
            if isinstance(relationship, relationship_factory.relationship):
                self.relationships.append(relationship)
            else:
                print("SYSTEM ERROR non relationship in list of relationships to be set")

    def add_node(self, node, node_type=None):
        if isinstance(node, node_factory.node if node_type is None else node_type):
            if node.node_id not in self.nodes.keys():
                self.nodes[node.node_id] = node
                return True
            else:
                return False
        else:
            print('Internal Error, tried to add non node to network nodes list')
            sys.exit()

    def add_relationship(self, relationship, relationship_type=None):
        if isinstance(
                relationship, relationship_factory.relationship if relationship_type is None else relationship_type):

            self.relationships.append(relationship)
        else:
            print('Internal Error, tried to add non relationship to network relationships list')
            sys.exit()

    def add_ch_company(self, entity):
        self.add_node(entity, node_type=node_factory.ch_company)

    def add_ch_officer(self, ch_officer):
        self.add_node(ch_officer, node_type=node_factory.ch_officer)

    def add_ch_appointment(self, appointment):
        self.add_relationship(appointment, relationship_factory.ch_appointment)

    @classmethod
    def start(cls, ch_officer_ids, ch_company_numbers):
        print('Getting core Companies House Officers')
        core_ch_officers = [node_factory.ch_officer.init_from_id(
            ch_officer_id, appointments_limit=100) for ch_officer_id in ch_officer_ids]

        core_ch_companies = [node_factory.ch_company.init_from_company_number(
            ch_company_number) for ch_company_number in ch_company_numbers]

        nodes = core_ch_companies + core_ch_officers

        nodes_dict = {node.node_id: node for node in nodes}

        network = cls(nodes=nodes_dict)

        network.expand_network()

        return network

    def expand_network(self):

        new_nodes = self.nodes.copy()
        new_relationships = self.relationships.copy()

        for node in self.nodes.values():

            if node.expanded:
                continue

            new_node_relationship_tuples = expand.expand_node(node, new_nodes, new_relationships)

            for new_node_relationship_tuple in new_node_relationship_tuples:
                new_node = new_node_relationship_tuple[0]
                new_relationship = new_node_relationship_tuple[1]

                new_nodes[new_node.node_id] = new_node
                new_relationships.append(new_relationship)

        self.set_nodes(new_nodes)
        self.set_relationships(new_relationships)

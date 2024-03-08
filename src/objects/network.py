import json
import sys
from .graph_objects.nodes import node_factory
from .graph_objects.relationships import relationship_factory
from .graph_objects import expand
from .graph_objects.nodes.offshore_leaks import init_offshore_leaks_nodes
import pandas as pd
import uuid


class Network:
    clear_network_strings = ('match (a) -[r] -> () delete a, r', 'match (a) delete a',)

    def __init__(self, nodes=None, relationships=None, name='', network_uuid=''):
        self.network_uuid = str(uuid.uuid4()) if network_uuid == '' else network_uuid
        self.name = name
        self.nodes = {} if nodes is None else nodes
        self.relationships = [] if relationships is None else relationships

    # Getters

    def get_nodes_of_type(self, node_type, inverse=False):

        found_nodes = {}
        exclude_nodes = {}

        for node_id, node in self.nodes.items():
            if isinstance(node, node_type):
                found_nodes[node_id] = node
            else:
                exclude_nodes[node_id] = node
        if inverse:
            return exclude_nodes
        else:
            return found_nodes

    def get_relationships_of_type(self, relationship_type, inverse=False):
        found_relationships = []
        exclude_relationships = []

        for relationship in self.relationships:
            if isinstance(relationship, relationship_type):
                found_relationships.append(relationship)
            else:
                exclude_relationships.append(relationship)

        if inverse:
            return exclude_relationships
        else:
            return found_relationships

    def get_node(self, node_id):
        if node_id in self.nodes.keys():
            return self.nodes[node_id]
        else:
            print("Internal ERROR {0} node not in network".format(node_id))
            return None

    def node_in_network(self, node_id):
        if node_id in self.nodes.keys():
            return True
        else:
            return False

    @property
    def ch_officers(self):
        return self.get_nodes_of_type(node_type=node_factory.ch_officer)

    @property
    def ch_companies(self):
        return self.get_nodes_of_type(node_type=node_factory.ch_company)

    @property
    def ol_nodes(self):
        return self.get_nodes_of_type(node_type=node_factory.ol_node)

    @property
    def non_ol_nodes(self):
        return self.get_nodes_of_type(node_type=node_factory.ol_node, inverse=True)

    @property
    def ol_addresses(self):
        return self.get_nodes_of_type(node_type=node_factory.ol_address)

    @property
    def ol_entities(self):
        return self.get_nodes_of_type(node_type=node_factory.ol_entity)

    @property
    def ol_intermediaries(self):
        return self.get_nodes_of_type(node_type=node_factory.ol_intermediary)

    @property
    def ol_officers(self):
        return self.get_nodes_of_type(node_type=node_factory.ol_officer)

    @property
    def ol_others(self):
        return self.get_nodes_of_type(node_type=node_factory.ol_other)

    @property
    def ch_appointments(self):
        return self.get_relationships_of_type(relationship_type=relationship_factory.ch_appointment)

    @property
    def regulated_donees(self):
        return self.get_nodes_of_type(node_type=node_factory.ec_regulated_donee)

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

    def add_ch_company(self, ch_company):
        self.add_node(ch_company, node_type=node_factory.ch_company)

    def add_ch_officer(self, ch_officer):
        self.add_node(ch_officer, node_type=node_factory.ch_officer)

    def add_ol_node(self, ol_node):
        self.add_node(ol_node, node_type=node_factory.ol_node)

    def add_ol_address(self, ol_address):
        self.add_node(ol_address, node_type=node_factory.ol_address)

    def add_ol_entity(self, ol_entity):
        self.add_node(ol_entity, node_type=node_factory.ol_entity)

    def add_ol_intermediary(self, ol_intermediary):
        self.add_node(ol_intermediary, node_type=node_factory.ol_intermediary)

    def add_ol_officer(self, ol_officer):
        self.add_node(ol_officer, node_type=node_factory.ol_officer)

    def add_ol_other(self, ol_other):
        self.add_node(ol_other, node_type=node_factory.ol_other)

    def add_regulated_donee(self, regulated_donee):
        self.add_node(regulated_donee, node_type=node_factory.ec_regulated_donee)

    def add_ch_appointment(self, appointment):
        self.add_relationship(appointment, relationship_factory.ch_appointment)

    def add_same_as(self, same_as_relationship):
        self.add_relationship(same_as_relationship, relationship_factory.same_as)

    def add_electoral_commission_donation_relationship(self, electoral_commission_donation_relationship):
        self.add_relationship(electoral_commission_donation_relationship, relationship_factory.ec_donation)

    @classmethod
    def start(cls, ch_officer_ids, ch_company_numbers, offshore_leaks_node_ids, network_name):

        nodes = []

        if len(ch_officer_ids) > 0:
            print('Getting core Companies House Officers')
            core_ch_officers = [node_factory.ch_officer.init_from_id(
                ch_officer_id) for ch_officer_id in ch_officer_ids]
            nodes += core_ch_officers

        if len(ch_company_numbers) > 0:
            print('Getting core Companies House Companies')
            core_ch_companies = [node_factory.ch_company.init_from_company_number(
                ch_company_number) for ch_company_number in ch_company_numbers]
            nodes += core_ch_companies

        if len(offshore_leaks_node_ids) > 0:
            print('Getting core Offshore Leaks nodes')
            core_ol_nodes = init_offshore_leaks_nodes.init_nodes_from_ids(node_ids=offshore_leaks_node_ids)
            nodes += core_ol_nodes

        nodes_dict = {node.node_id: node for node in nodes}

        network = cls(nodes=nodes_dict, name=network_name)

        network.expand_network()

        return network

    def expand_network(self, target_node_ids=None):

        target_node_ids = self.nodes.keys() if target_node_ids is None else target_node_ids

        new_nodes = self.nodes.copy()
        new_relationships = self.relationships.copy()

        for node in self.nodes.values():

            if node.expanded or node.node_id not in target_node_ids:
                continue

            new_node_relationship_tuples = expand.expand_node(node, new_nodes)

            for new_node_relationship_tuple in new_node_relationship_tuples:

                new_node = new_node_relationship_tuple[0]
                new_relationship = new_node_relationship_tuple[1]

                if self.relationship_already_exists(new_relationship, new_relationships):
                    continue
                else:
                    new_nodes[new_node.node_id] = new_node
                    new_relationships.append(new_relationship)

        self.set_nodes(new_nodes)
        self.set_relationships(new_relationships)

    def to_dataframes(self):
        df_dict = {'ch_officers': pd.DataFrame([o.to_flat_dict() for o in self.ch_officers.values()]).drop(
            columns=['items', 'links_self']),
            'ch_companies': pd.DataFrame(c.to_flat_dict() for c in self.ch_companies.values()),
            'ch_appointments': pd.DataFrame([a.to_flat_dict() for a in self.ch_appointments]),
        }
        return df_dict

    def save_csvs(self, directory_path):
        dfs = self.to_dataframes()

        for attr, df in dfs.items():
            path = directory_path + '/{attr}.csv'.format(attr=attr)
            df.to_csv(path, index=False)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def save_json(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self, f, default=lambda o: o.__dict__,
                      sort_keys=True, ensure_ascii=False)

    def save_xlsx(self, path):

        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        dfs = self.to_dataframes()

        for sheet, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

        writer.close()

    def render_create_cypher(self):

        node_cyphers = self.get_node_cyphers()

        nodes_string = ''

        for i in range(len(node_cyphers)):
            if i > 0:
                nodes_string += ', '

            nodes_string += '{node}'.format(node=node_cyphers[i])

        cypher_string = '''
        CREATE {nodes}
        '''.format(nodes=nodes_string)

        cypher_string += self.get_relationship_cypher()

        return cypher_string

    @classmethod
    def from_dict(cls, network_dict):
        return cls(name=network_dict['name'],
                   network_uuid=network_dict['network_uuid'],
                   relationships=[relationship_factory.relationship_dict[relationship['relationship_type']]
                                  (**relationship) for relationship in network_dict.get('relationships', [])],
                   nodes={node_id: node_factory.node_dict[node['node_type']](**node) for node_id, node in
                          network_dict.get('nodes', {}).items()}
                   )

    @classmethod
    def load_json(cls, path):
        with open(path) as f:
            data = json.load(f)

        return cls.from_dict(data)

    def get_node_cyphers(self):
        node_cyphers = []
        for node in self.nodes.values():
            clause = node.render_create_clause()
            node_cyphers.append(clause)
        return node_cyphers

    def get_relationship_cypher(self):
        cypher = ''
        for relationship in self.relationships:
            cypher += '\n {clause}'.format(clause=relationship.render_create_clause())
        return cypher

    def create_electoral_commission_donation_relationship(self, parent_node_id, child_node_id, attributes):
        parent_node = self.get_node(parent_node_id)
        child_node = self.get_node(child_node_id)

        if parent_node is None or child_node is None:
            print('System Error: electoral_commission_donation relationship nodes aren\'t in network')
            return None

        relationship = relationship_factory.ec_donation(parent_node_name=parent_node.unique_label,
                                                        parent_id=parent_node.node_id,
                                                        child_node_name=child_node.unique_label,
                                                        child_id=child_node.node_id,
                                                        **attributes
                                                        )

        if self.relationship_already_exists(new_relationship=relationship, existing_relationships=self.relationships):
            print('relationship already exists')
            return None
        else:
            self.add_electoral_commission_donation_relationship(relationship)

    def create_same_as_relationship(self, parent_node_id, child_node_id):
        parent_node = self.get_node(parent_node_id)
        child_node = self.get_node(child_node_id)

        if parent_node is None or child_node is None:
            print('System Error: same relationship nodes aren\'t in network')
            return None

        kwargs = {'child': {x: child_node.__dict__[x] for x in child_node.__dict__ if x != 'node_id'},
                  'parent': {x: parent_node.__dict__[x] for x in parent_node.__dict__ if x != 'node_id'}
                  }

        relationship = relationship_factory.same_as(parent_node_name=parent_node.unique_label,
                                                    parent_id=parent_node.node_id,
                                                    child_node_name=child_node.unique_label,
                                                    child_id=child_node.node_id,
                                                    **kwargs
                                                    )

        if self.relationship_already_exists(new_relationship=relationship, existing_relationships=self.relationships):
            print('relationship already exists')
            return None
        else:
            self.add_same_as(relationship)

    @classmethod
    def relationship_already_exists(cls, new_relationship, existing_relationships):
        flat_new_relationship = new_relationship.to_flat_dict()

        already_exists = False

        for relationship in existing_relationships:
            identical = True

            flat_relationship = relationship.to_flat_dict()

            for key, value in flat_relationship.items():
                if flat_new_relationship.get(key, None) != value:
                    identical = False
                    break

            if identical:
                already_exists = True
                break

        return already_exists

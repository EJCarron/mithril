import json
import sys
from .graph_objects.nodes import node_factory
from .graph_objects.relationships import relationship_factory
from src.scripts.OffshoreLeaks import offshore_leaks_api
from src.scripts.uk_electoral_commission import electoral_commission_api
import pandas as pd
import uuid
from src.scripts.generate_node_id import generate_node_id


def split_node_instructions_by_type(nodes):
    nodes_by_type = {}

    for node_instructions in nodes:
        if node_instructions['node_type'] not in nodes_by_type.keys():
            nodes_by_type[node_instructions['node_type']] = []
        nodes_by_type[node_instructions['node_type']].append(node_instructions['node_id'])

    return nodes_by_type


def split_nodes_by_high_level_type(nodes):
    nodes_by_type = {node_type: [] for node_type in node_factory.high_level_types_dict.keys()}

    for node in nodes:
        found_type = False
        for high_level_node_type_str, high_level_node_type in node_factory.high_level_types_dict.items():
            if issubclass(type(node), high_level_node_type):
                nodes_by_type[high_level_node_type_str].append(node)
                found_type = True
                break
        if not found_type:
            print(f'SYSTEM ERROR could not find high level type for {node.name} of type {type(node).__name__}')

    return nodes_by_type


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

    def get_same_as_relationships(self):
        return self.get_relationships_of_type(relationship_factory.same_as)

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
        return self.get_nodes_of_type(node_type=node_factory.ec_regulated_entity)

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
        self.add_node(regulated_donee, node_type=node_factory.ec_regulated_entity)

    def add_ch_appointment(self, appointment):
        self.add_relationship(appointment, relationship_factory.ch_appointment)

    def add_same_as(self, same_as_relationship):
        self.add_relationship(same_as_relationship, relationship_factory.same_as)

    def add_electoral_commission_donation_relationship(self, electoral_commission_donation_relationship):
        self.add_relationship(electoral_commission_donation_relationship, relationship_factory.ec_donation)

    @classmethod
    def start(cls, core_nodes, network_name):

        nodes_by_type = split_node_instructions_by_type(core_nodes)

        nodes = []

        for node_type, node_ids in nodes_by_type.items():
            nodes += node_factory.node_dict[node_type].batch_init(node_ids)

        nodes_dict = {node.node_id: node for node in nodes}

        network = cls(nodes=nodes_dict, name=network_name)

        network.expand()

        return network

    # def expand_network(self, target_node_ids=None):
    #
    #     target_node_ids = self.nodes.keys() if target_node_ids is None else target_node_ids
    #
    #     new_nodes = self.nodes.copy()
    #     new_relationships = self.relationships.copy()
    #
    #     for node in self.nodes.values():
    #
    #         if node.expanded or node.node_id not in target_node_ids:
    #             continue
    #
    #         new_node_relationship_tuples = expand_old.expand_node(node, new_nodes)
    #
    #         for new_node_relationship_tuple in new_node_relationship_tuples:
    #
    #             new_node = new_node_relationship_tuple[0]
    #             new_relationship = new_node_relationship_tuple[1]
    #
    #             if self.relationship_already_exists(new_relationship, new_relationships):
    #                 continue
    #             else:
    #                 new_nodes[new_node.node_id] = new_node
    #                 new_relationships.append(new_relationship)
    #
    #     self.set_nodes(new_nodes)
    #     self.set_relationships(new_relationships)

    def expand(self, target_node_ids=None):

        nodes_to_expand = self.nodes.values() if target_node_ids is None else [self.get_node(node_id) for node_id in
                                                                               target_node_ids]

        nodes_to_expand = [node for node in nodes_to_expand if not node.expanded]

        nodes_to_expand_split_by_type = split_nodes_by_high_level_type(nodes_to_expand)

        self.expand_ch_nodes(nodes_to_expand_split_by_type[node_factory.ch_node_str])
        self.expand_ol_nodes(nodes_to_expand_split_by_type[node_factory.ol_node_str])
        self.expand_ec_nodes(nodes_to_expand_split_by_type[node_factory.ec_node_str])

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

        if self.relationship_already_exists(new_relationship=relationship):
            print('relationship already exists')
            return None
        else:
            self.add_electoral_commission_donation_relationship(relationship)

    def find_same_as_centre(self, node_id):
        same_as_relationships = self.get_same_as_relationships()

        same_as_centre_ids = []

        for relationship in same_as_relationships:
            if node_id == relationship.parent_id:
                if relationship.centre_node_id not in same_as_centre_ids:
                    same_as_centre_ids.append(relationship.centre_node_id)

        if len(same_as_centre_ids) == 0:
            return None
        if len(same_as_centre_ids) > 1:
            print(f'SYSTEM ERROR node {self.get_node(node_id).name} attached to {len(same_as_centre_ids)} centres')
            exit()

        return self.get_node(same_as_centre_ids[0])

    def remove_same_as_centre_and_reassign_to_new_centre(self, centre_to_remove, new_centre):
        relationships = self.get_same_as_relationships()

        for relationship in relationships:
            if relationship.centre_node_id == centre_to_remove.node_id:
                relationship.change_centre(new_centre)

    def create_same_as_relationship(self, first_node_id, second_node_id):
        first_node = self.get_node(first_node_id)
        second_node = self.get_node(second_node_id)

        if first_node is None or second_node is None:
            print('System Error: same relationship nodes aren\'t in network')
            return None

        first_node_already_existing_associated_centre = self.find_same_as_centre(first_node_id)
        second_node_already_existing_associated_centre = self.find_same_as_centre(second_node_id)

        if first_node_already_existing_associated_centre is None and second_node_already_existing_associated_centre is None:
            same_as_centre = node_factory.same_as_centre(name=first_node.name)
            self.add_node(same_as_centre)
        elif first_node_already_existing_associated_centre is not None and second_node_already_existing_associated_centre is None:
            same_as_centre = first_node_already_existing_associated_centre
        elif first_node_already_existing_associated_centre is None and second_node_already_existing_associated_centre is not None:
            same_as_centre = second_node_already_existing_associated_centre
        else:
            self.remove_same_as_centre_and_reassign_to_new_centre(
                centre_to_remove=second_node_already_existing_associated_centre,
                new_centre=first_node_already_existing_associated_centre)
            return

        first_relationship = relationship_factory.same_as.create(same_as_centre=same_as_centre, node=first_node)
        second_relationship = relationship_factory.same_as.create(same_as_centre=same_as_centre, node=second_node)

        if not self.relationship_already_exists(new_relationship=first_relationship):
            self.add_same_as(first_relationship)

        if not self.relationship_already_exists(second_relationship):
            self.add_same_as(second_relationship)

    def relationship_already_exists(self, new_relationship):
        flat_new_relationship = new_relationship.to_flat_dict()

        already_exists = False

        for relationship in self.relationships:
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

    def expand_ch_nodes(self, nodes):

        for node in nodes:
            if type(node).__name__ == node_factory.ch_officer_str:
                self.expand_ch_officer(node)
            elif type(node).__name__ == node_factory.ch_company_str:
                self.expand_ch_company(node)
            else:
                print(f"SYSTEM ERROR node not either ch company or officer {node.name} of type {type(node).__name__}")

    def expand_ch_officer(self, ch_officer):
        print('expanding CH Officer ' + ch_officer.name)

        for item in ch_officer.items:
            company_number = item['appointed_to']['company_number']
            company_node_id = generate_node_id(str(company_number), node_factory.ch_company_str)
            if company_node_id in self.nodes.keys():
                ch_company = self.get_node(company_node_id)
            else:
                ch_company = node_factory.ch_company.init_from_companies_house_id(company_number)
                self.add_node(ch_company)

            ch_appointment = relationship_factory.ch_appointment(parent_node_name=ch_officer.unique_label,
                                                                 child_node_name=ch_company.unique_label,
                                                                 parent_id=ch_officer.node_id,
                                                                 child_id=ch_company.node_id,
                                                                 **item)

            if not self.relationship_already_exists(ch_appointment):
                self.add_relationship(ch_appointment)

        ch_officer.expanded = True

    def expand_ch_company(self, ch_company):
        print('expanding CH Company ' + ch_company.name)

        ch_officer_ids = ch_company.get_officer_ids()

        for ch_officer_id in ch_officer_ids:
            node_id = generate_node_id(ch_officer_id, node_factory.ch_officer_str)
            if node_id in self.nodes.keys():
                ch_officer = self.get_node(node_id)
            else:
                ch_officer = node_factory.ch_officer.init_from_companies_house_id(ch_officer_id)

                self.add_ch_officer(ch_officer)

            item = ch_officer.get_item_from_company_number(ch_company.company_number)

            if item is None:
                print('ERROR appointment to {0} not found in {1}\'s appointment list'.format(ch_company.name,
                                                                                             ch_officer.name))
                item = {}

            ch_appointment = relationship_factory.ch_appointment(parent_node_name=ch_officer.unique_label,
                                                                 child_node_name=ch_company.unique_label,
                                                                 parent_id=ch_officer.node_id,
                                                                 child_id=ch_company.node_id,
                                                                 **item)

            if not self.relationship_already_exists(ch_appointment):
                self.add_relationship(ch_appointment)

        self.company_donations_connections(ch_company)

        ch_company.expanded = True

    def company_donations_connections(self, company):
        donors = self.find_ch_company_in_ec_donors(company.company_number)

        for donor in donors:
            if donor.node_id not in self.nodes.keys():
                self.add_node(donor)
            self.create_same_as_relationship(company.node_id, donor.node_id)

    def find_ch_company_in_ec_donors(self, company_number):
        raw_donors = electoral_commission_api.get_donors_by_company_number(company_number)
        if len(raw_donors) > 0:
            donors = [node_factory.ec_donor(**raw_donor) for raw_donor in raw_donors]
            return donors
        return []

    def expand_ol_nodes(self, nodes):
        if len(nodes) == 0:
            return
        print('expanding OffshoreLeaks nodes ')
        self.expand_local_db_nodes(nodes=nodes, api=offshore_leaks_api,
                                   relationship_type=relationship_factory.ol_relationship)

    def expand_ec_nodes(self, nodes):
        if len(nodes) == 0:
            return
        print('expanding Electoral Commission nodes')
        self.expand_local_db_nodes(nodes=nodes, api=electoral_commission_api,
                                   relationship_type=relationship_factory.ec_donation)

        for node in nodes:
            if isinstance(node, node_factory.ec_donor) and node.CompanyRegistrationNumber is not None:
                self.ec_donor_company_expand(node)

    def ec_donor_company_expand(self, node):
        company_number = node.CompanyRegistrationNumber
        company_node_id = generate_node_id(company_number, node_factory.ch_company_str)

        if company_node_id not in self.nodes.keys():
            company = node_factory.ch_company.init_from_companies_house_id(company_number)
            if company is None:
                return
            self.add_node(company)

        self.create_same_as_relationship(node.node_id, company_node_id)

    def expand_local_db_nodes(self, nodes, api, relationship_type):
        raw_relationships = api.get_relationships(node_ids=[node.node_id for node in nodes])

        node_ids_to_pull = self.find_nodes_to_pull(raw_relationships)

        new_nodes = api.get_nodes(node_ids_to_pull)

        if len(new_nodes) > 0:
            [self.add_node(node_factory.node_dict[node['obj_type']](**node)) for node in new_nodes]

        for raw_relationship in raw_relationships:
            parent_node = self.get_node(raw_relationship['parent_node_id'])
            child_node = self.get_node(raw_relationship['child_node_id'])

            if parent_node is None or child_node is None:
                continue

            new_relationship = relationship_type(parent_node_name=parent_node.unique_label,
                                                 parent_id=parent_node.node_id,
                                                 child_node_name=child_node.unique_label,
                                                 child_id=child_node.node_id,
                                                 **raw_relationship
                                                 )

            if not self.relationship_already_exists(new_relationship):
                self.add_relationship(new_relationship, relationship_type)

        for node in nodes:
            node.expanded = True

    def find_nodes_to_pull(self, raw_relationships):
        node_ids_to_pull = []

        for raw_relationship in raw_relationships:

            def need_to_pull(node_id):
                if node_id in self.nodes.keys() or node_id in node_ids_to_pull:
                    pass
                else:
                    node_ids_to_pull.append(node_id)

            need_to_pull(raw_relationship['parent_node_id'])
            need_to_pull(raw_relationship['child_node_id'])

        return node_ids_to_pull

    def add_nodes(self, add_nodes):
        nodes_not_in_network = [node for node in add_nodes if node['node_id'] not in self.nodes.keys()]
        nodes_split_by_type = split_node_instructions_by_type(nodes_not_in_network)

        nodes = []

        for node_type, node_ids in nodes_split_by_type.items():
            nodes += node_factory.node_dict[node_type].batch_init(node_ids)

        [self.add_node(node) for node in nodes]

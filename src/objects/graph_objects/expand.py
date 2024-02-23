from .nodes import node_factory
from .relationships import relationship_factory
from src.scripts.OffshoreLeaks import offshore_leaks_api


def expand_node(node, existing_nodes, existing_relationships):
    if isinstance(node, node_factory.ch_officer):
        return expand_ch_officer(node, existing_nodes, existing_relationships)
    elif isinstance(node, node_factory.ch_company):
        return expand_ch_company(node, existing_nodes, existing_relationships)
    elif isinstance(node, node_factory.ol_node):
        return expand_ol_node(node, existing_nodes, existing_relationships)
    else:
        print('System ERROR haven\'t implement expand for ' + node.node_type)
        return None, None


def expand_ol_node(node, existing_nodes, existing_relationships):
    raw_relationships = offshore_leaks_api.get_relationships(db_node_id=node.db_node_id)

    new_node_relationship_tuples = []

    for raw_relationship in raw_relationships:
        parent_node = None
        child_node = None

        if raw_relationship['node_id_start'] == node.db_node_id:
            related_node_db_id = raw_relationship['node_id_end']
            parent_node = node
        else:
            related_node_db_id = raw_relationship['node_id_start']
            child_node = node

        if ('ol_' + str(related_node_db_id)) in existing_nodes.keys():
            related_node = existing_nodes['ol_' + str(related_node_db_id)]
        else:
            raw_node = offshore_leaks_api.get_nodes([related_node_db_id])[0]
            related_node = node_factory.node_dict[raw_node['node_type']](**raw_node)

        if parent_node is None:
            parent_node = related_node
        else:
            child_node = related_node

        new_relationship = relationship_factory.ol_relationship(parent_node_name=parent_node.unique_label,
                                                                parent_id=parent_node.node_id,
                                                                child_node_name=child_node.unique_label,
                                                                child_id=child_node.node_id,
                                                                **raw_relationship
                                                                )

        if relationship_already_exists(new_relationship, existing_relationships):
            continue
        else:
            new_node_relationship_tuples.append((related_node, new_relationship))

    return new_node_relationship_tuples


def expand_ch_company(ch_company, existing_nodes, existing_relationships):
    print('expanding CH Company ' + ch_company.company_name)

    new_officer_appointment_tuples = []

    ch_officer_ids = ch_company.get_officer_ids()

    for ch_officer_id in ch_officer_ids:
        if ch_officer_id in existing_nodes.keys():
            ch_officer = existing_nodes[ch_officer_id]
        else:
            ch_officer = node_factory.ch_officer.init_from_id(ch_officer_id)

        item = ch_officer.get_item_from_company_number(ch_company.company_number)

        if item is None:
            print('ERROR appointment to {0} not found in {1}\'s appointment list'.format(ch_company.company_name,
                                                                                         ch_officer.name))
            continue

        ch_appointment = relationship_factory.ch_appointment(parent_node_name=ch_officer.unique_label,
                                                             child_node_name=ch_company.unique_label,
                                                             parent_id=ch_officer.node_id, child_id=ch_company.node_id,
                                                             **item)
        if relationship_already_exists(ch_appointment, existing_relationships):
            continue
        else:
            new_officer_appointment_tuples.append((ch_officer, ch_appointment))

    ch_company.expanded = True

    return new_officer_appointment_tuples


def expand_ch_officer(ch_officer, existing_nodes, existing_relationships):
    print('expanding CH Officer ' + ch_officer.name)

    new_company_appointment_tuples = []

    for item in ch_officer.items:
        company_number = item['appointed_to']['company_number']
        if company_number not in existing_nodes.keys():
            ch_company = node_factory.ch_company.init_from_company_number(company_number)

        else:
            ch_company = existing_nodes[company_number]

        ch_appointment = relationship_factory.ch_appointment(parent_node_name=ch_officer.unique_label,
                                                             child_node_name=ch_company.unique_label,
                                                             parent_id=ch_officer.node_id, child_id=ch_company.node_id,
                                                             **item)

        if relationship_already_exists(ch_appointment, existing_relationships):
            continue
        else:
            new_company_appointment_tuples.append((ch_company, ch_appointment))

    ch_officer.expanded = True

    return new_company_appointment_tuples


def relationship_already_exists(new_relationship, existing_relationships):
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

from src.objects.graph_objects.nodes.companies_house.companies_house_officer import CompaniesHouseOfficer
from src.objects.graph_objects.nodes.companies_house.companies_house_company import CompaniesHouseCompany
from src.objects.graph_objects.nodes.offshore_leaks.offshore_leaks_node import OffshoreLeaksNode
from src.objects.graph_objects.nodes.offshore_leaks.offshore_leaks_address import OffshoreLeaksAddress
from src.objects.graph_objects.nodes.offshore_leaks.offshore_leaks_entity import OffshoreLeaksEntity
from src.objects.graph_objects.nodes.offshore_leaks.offshore_leaks_intermediary import OffshoreLeaksIntermediary
from src.objects.graph_objects.nodes.offshore_leaks.offshore_leaks_officer import OffshoreLeaksOfficer
from src.objects.graph_objects.nodes.offshore_leaks.offshore_leaks_other import OffshoreLeaksOther
from .node import Node

node_str = Node.__name__
ch_officer_str = CompaniesHouseOfficer.__name__
ch_company_str = CompaniesHouseCompany.__name__
ol_node_str = OffshoreLeaksNode.__name__
ol_address_str = OffshoreLeaksAddress.__name__
ol_entity_str = OffshoreLeaksEntity.__name__
ol_intermediary_str = OffshoreLeaksIntermediary.__name__
ol_officer_str = OffshoreLeaksOfficer.__name__
ol_other_str = OffshoreLeaksOther.__name__

node = Node
ch_officer = CompaniesHouseOfficer
ch_company = CompaniesHouseCompany
ol_node = OffshoreLeaksNode
ol_address = OffshoreLeaksAddress
ol_entity = OffshoreLeaksEntity
ol_intermediary = OffshoreLeaksIntermediary
ol_officer = OffshoreLeaksOfficer
ol_other = OffshoreLeaksOther

node_dict = {node_str: node,
             ch_officer_str: ch_officer,
             ch_company_str: ch_company,
             ol_node_str: ol_node,
             ol_address_str: ol_address,
             ol_entity_str: ol_entity,
             ol_intermediary_str: ol_intermediary,
             ol_officer_str: ol_officer,
             ol_other_str: ol_other
             }

ol_list = [ol_address, ol_entity, ol_intermediary, ol_officer, ol_other]

ol_raw_address_keys = ['ol_node_id', 'address', 'name', 'countries', 'country_codes', 'sourceID', 'valid_until', 'note']

ol_raw_entity_keys = ['ol_node_id', 'name', 'original_name', 'former_name', 'jurisdiction', 'jurisdiction_description',
                      'company_type', 'address', 'internal_id', 'incorporation_date', 'inactivation_date',
                      'struck_off_date', 'dorm_date', 'status', 'service_provider', 'ibcRUC', 'country_codes',
                      'countries',
                      'sourceID',
                      'valid_until', 'note']

ol_raw_intermediary_keys = ['ol_node_id', 'name', 'status', 'internal_id', 'address', 'countries', 'country_codes',
                            'sourceID',
                            'valid_until', 'note']

ol_raw_officer_keys = ['ol_node_id', 'name', 'countries', 'country_codes', 'sourceID', 'valid_until', 'note']

ol_raw_other_keys = ['ol_node_id', 'name', 'type', 'incorporation_date', 'struck_off_date', 'closed_date',
                     'jurisdiction',
                     'jurisdiction_description',
                     'countries', 'country_codes', 'sourceID', 'valid_until', 'note']

ol_keys_dict = {ol_address_str: ol_raw_address_keys,
                ol_entity_str: ol_raw_entity_keys,
                ol_intermediary_str: ol_raw_intermediary_keys,
                ol_officer_str: ol_raw_officer_keys,
                ol_other_str: ol_raw_other_keys
                }

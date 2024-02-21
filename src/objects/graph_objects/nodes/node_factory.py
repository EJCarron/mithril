from .companies_house_officer import CompaniesHouseOfficer
from .companies_house_company import CompaniesHouseCompany
from .node import Node

node_str = Node.__name__
ch_officer_str = CompaniesHouseOfficer.__name__
ch_company_str = CompaniesHouseCompany.__name__

node = Node
ch_officer = CompaniesHouseOfficer
ch_company = CompaniesHouseCompany

node_dict = {node_str: node,
             ch_officer_str: ch_officer,
             ch_company_str: ch_company
             }

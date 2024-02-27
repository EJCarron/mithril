from src.objects.graph_objects.nodes.node import Node
from src.scripts.companies_house import companies_house_api


class CompaniesHouseCompany(Node):

    def __init__(self, **kwargs):
        super(CompaniesHouseCompany, self).__init__()
        self.node_id = None
        self.name = None
        self.__dict__.update(kwargs)

    @property
    def address(self):
        return ' '.join(self.registered_office_address.values())

    def render_unique_label(self):
        unique_label = '{name}_{id}'.format(name=self.name.replace(' ', '_'), id=self.node_id)
        return unique_label

    @classmethod
    def from_api_result(cls, result):
        result['name'] = cls.clean_name(result['company_name'])
        result['node_id'] = result['company_number']
        return cls(**result)

    @classmethod
    def init_from_company_number(cls, ch_company_number):
        print('Pulling data for {0} from Companies House API'.format(ch_company_number))
        raw_result = companies_house_api.get_company(ch_company_number)

        if raw_result is None:
            return None

        return cls.from_api_result(raw_result)

    def get_officer_ids(self):
        return companies_house_api.get_company_officer_ids(self.node_id)

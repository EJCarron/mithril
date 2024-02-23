from src.objects.graph_objects.nodes.node import Node
from src.scripts.companies_house import companies_house_api


class CompaniesHouseCompany(Node):

    def __init__(self, **kwargs):
        super(CompaniesHouseCompany, self).__init__()
        self.company_number = None
        self.company_name = None
        self.__dict__.update(kwargs)

    @property
    def node_id(self):
        return self.company_number

    def render_unique_label(self):
        unique_label = '{name}_{id}'.format(name=self.company_name.replace(' ', '_'), id=self.company_number)
        return unique_label

    @classmethod
    def from_api_result(cls, result):
        result['company_name'] = cls.clean_name(result['company_name'])
        return cls(**result)

    @classmethod
    def init_from_company_number(cls, ch_company_number):
        print('Pulling data for {0} from Companies House API'.format(ch_company_number))
        raw_result = companies_house_api.get_company(ch_company_number)

        if raw_result is None:
            return None

        return cls.from_api_result(raw_result)

    def get_officer_ids(self):
        return companies_house_api.get_company_officer_ids(self.company_number)

from src.objects.graph_objects.nodes.companies_house.companies_house_node import CompaniesHouseNode
from src.scripts.companies_house import companies_house_api
from src.scripts.generate_node_id import generate_node_id


class CompaniesHouseCompany(CompaniesHouseNode):

    def __init__(self, **kwargs):
        self.registered_office_address = None
        self.node_id = None
        self.name = None
        self.company_number = None
        super(CompaniesHouseCompany, self).__init__(**kwargs)
        self.init_token = self.company_number

    @property
    def events(self):
        events = []

        if 'date_of_creation' in self.__dict__.keys():
            date_split = self.date_of_creation.split('-')

            events.append({'event': f'{self.name} was registered with Companies House',
                           'day': int(date_split[2]),
                           'month': int(date_split[1]),
                           'year': int(date_split[0])
                           })

        if 'date_of_cessation' in self.__dict__.keys():
            date_split = self.date_of_cessation.split('-')

            events.append({'event': f'{self.name} was removed from the Companies House register',
                           'day': date_split[2],
                           'month': date_split[1],
                           'year': date_split[0]
                           })

        return events

    @property
    def address(self):
        return ' '.join(self.registered_office_address.values())

    def render_unique_label(self):
        unique_label = '{name}_{id}'.format(name=self.name.replace(' ', '_'), id=self.company_number)
        return unique_label

    @classmethod
    def from_api_result(cls, result):
        result['name'] = cls.clean_name(result['company_name'])
        type_str = CompaniesHouseCompany.__name__
        result['node_id'] = generate_node_id(result['company_number'], type_str)
        return cls(**result)

    @classmethod
    def init_from_companies_house_id(cls, ch_company_number):
        print('Pulling data for {0} from Companies House API'.format(ch_company_number))
        raw_result = companies_house_api.get_company(ch_company_number)

        if raw_result is None:
            return None

        return cls.from_api_result(raw_result)

    def get_officer_ids(self):
        return companies_house_api.get_company_officer_ids(self.company_number)

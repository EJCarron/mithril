from src.objects.graph_objects.nodes.node import Node
from src.scripts.companies_house import companies_house_api


class CompaniesHouseCompany(Node):

    def __init__(self, **kwargs):
        super(CompaniesHouseCompany, self).__init__()
        self.registered_office_address = None
        self.node_id = None
        self.name = None
        self.__dict__.update(kwargs)

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

    @classmethod
    def batch_init(cls, node_ids):
        nodes = []

        for node_id in node_ids:
            nodes.append(cls.init_from_company_number(node_id))

        return nodes

    def get_officer_ids(self):
        return companies_house_api.get_company_officer_ids(self.node_id)

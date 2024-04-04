from src.scripts.generate_node_id import generate_node_id
from src.scripts.companies_house import companies_house_api
from src.objects.graph_objects.nodes.companies_house.companies_house_node import CompaniesHouseNode


class CompaniesHouseOfficer(CompaniesHouseNode):

    def __init__(self, **kwargs):
        self.date_of_birth = {}
        self.name = None
        self.items = None
        super(CompaniesHouseOfficer, self).__init__(**kwargs)
        self.init_token = self.officer_id

    @property
    def events(self):
        events = []

        if 'date_of_birth' in self.__dict__.keys():
            if self.date_of_birth != {}:
                officer_born_event = {'event': f'{self.name} was born',
                                      'month': self.date_of_birth.get('month', None),
                                      'year': self.date_of_birth.get('year', None)
                                      }
                events.append(officer_born_event)

        return events

    @classmethod
    def init_from_companies_house_id(cls, ch_officer_id):
        print('Pulling data for {0} from Companies House API'.format(ch_officer_id))
        raw_result = companies_house_api.get_officer(officer_id=ch_officer_id)

        if raw_result is None:
            return None

        return cls.from_api_result(raw_result)

    @classmethod
    def from_api_result(cls, result):
        result['officer_id'] = companies_house_api.extract_id_from_link(result['links']['self'])
        result['node_id'] = generate_node_id(result['officer_id'], CompaniesHouseOfficer.__name__)
        result['name'] = cls.clean_name(result['name'])

        new_officer = cls(**result)

        return new_officer


    def get_item_from_company_number(self, company_number):
        found_item = None

        for item in self.items:
            if item.get('appointed_to', {}).get('company_number', None) == company_number:
                found_item = item
                break

        return found_item

    def render_unique_label(self):
        unique_label = '{name}_{id}'.format(name=self.name.replace(' ', '_'), id=self.node_id)
        return unique_label

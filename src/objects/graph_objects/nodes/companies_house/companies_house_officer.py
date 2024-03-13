from src.objects.graph_objects.nodes.node import Node
from src.scripts.companies_house import companies_house_api


class CompaniesHouseOfficer(Node):

    def __init__(self, **kwargs):
        super(CompaniesHouseOfficer, self).__init__()
        self.date_of_birth = {}
        self.name = None
        self.items = None
        self.__dict__.update(kwargs)

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
    def init_from_id(cls, ch_officer_id):
        print('Pulling data for {0} from Companies House API'.format(ch_officer_id))
        raw_result = companies_house_api.get_officer(officer_id=ch_officer_id)

        if raw_result is None:
            return None

        return cls.from_api_result(raw_result)

    @classmethod
    def from_api_result(cls, result):
        result['node_id'] = companies_house_api.extract_id_from_link(result['links']['self'])
        result['name'] = cls.clean_name(result['name'])

        new_officer = cls(**result)

        return new_officer

    @classmethod
    def batch_init(cls, node_ids):
        nodes = []

        for node_id in node_ids:
            nodes.append(cls.init_from_id(node_id))

        return nodes

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

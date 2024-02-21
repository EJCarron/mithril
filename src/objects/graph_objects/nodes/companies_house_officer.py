from .node import Node
from ....scripts.companies_house import companies_house_api
from . import node_factory


class CompaniesHouseOfficer(Node):

    def __init__(self, **kwargs):
        super(CompaniesHouseOfficer, self).__init__()
        self.name = None
        self.officer_id = None
        self.items = None
        self.__dict__.update(kwargs)

    @property
    def node_id(self):
        return self.officer_id

    @classmethod
    def init_from_id(cls, ch_officer_id, appointments_limit):
        print('Pulling data for {0} from Companies House API'.format(ch_officer_id))
        raw_result = companies_house_api.get_officer(officer_id=ch_officer_id, appointments_limit=appointments_limit)

        if raw_result is None:
            return None

        return cls.from_api_result(raw_result)

    @classmethod
    def from_api_result(cls, result):
        result['officer_id'] = companies_house_api.extract_id_from_link(result['links']['self'])
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
        unique_label = '{name}_{id}'.format(name=self.name.replace(' ', '_'), id=self.officer_id)
        return unique_label

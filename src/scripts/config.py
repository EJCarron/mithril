import base64


class Config:
    def __init__(self, **kwargs):

        self.normal_key = ''
        self.__dict__.update(kwargs)

        self.appended = self.normal_key + ':'
        self.encoded = str(base64.b64encode(self.appended.encode()), 'utf-8')
        self.header = {'Authorization': 'Basic {0}'.format(self.encoded)}
        self.companies_house_api_base_url = 'https://api.company-information.service.gov.uk/'

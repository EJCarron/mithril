import base64


# todo refactor to seperate configs

# class CompaniesHouseConfig:
#     def __init__(self, normal_key, appointments_limit):
#         self.normal_key = normal_key
#         self.appointments_limit = appointments_limit
#
#         self.appended = self.normal_key + ':'
#         self.encoded = str(base64.b64encode(self.appended.encode()), 'utf-8')
#         self.header = {'Authorization': 'Basic {0}'.format(self.encoded)}
#
#
# class Neo4jConfig:
#     def __init__(self, uri, username, pw):
#         self.uri = uri
#         self.username = username
#         self.pw = pw


class Config:
    def __init__(self, normal_key, uri, username, pw):
        self.normal_key = normal_key
        self.uri = uri
        self.username = username
        self.pw = pw

        self.appended = self.normal_key + ':'
        self.encoded = str(base64.b64encode(self.appended.encode()), 'utf-8')
        self.header = {'Authorization': 'Basic {0}'.format(self.encoded)}

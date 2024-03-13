from src.objects.graph_objects.relationships.relationship import Relationship


class CompaniesHouseAppointment(Relationship):
    @property
    def events(self):
        officer_name = self.__dict__.get('name', self.parent_node_name)
        role = self.__dict__.get('officer_role', 'director')
        company = self.__dict__.get('appointed_to', {}).get('company_name', self.child_node_name)

        def prepare_event(date_str, event_text):
            if date_str is None:
                return None
            date_split = date_str.split('-')
            return {'day': int(date_split[2]),
             'month': int(date_split[1]),
             'year': int(date_split[0]),
             'event': event_text
             }

        events = [prepare_event(self.__dict__.get('appointed_on', None), f'{officer_name} was appointed as {role} to {company}'),
                  prepare_event(self.__dict__.get('appointed_before', None),
                                f'{officer_name} was appointed as {role} to {company} before this date.'),
                  prepare_event(self.__dict__.get('resign_on', None),
                                f'{officer_name} resigned as {role} at {company}')
                  ]

        events = [event for event in events if event is not None]
        return events

from ..relationship import Relationship


class OffshoreLeaksRelationship(Relationship):
    def render_create_clause(self):
        parameters_string = self.render_parameters_string()

        clause = '''
        CREATE ({parent})-[: {relationship} {{{parameters}}}]->({child})
        '''.format(parent=self.clean_name(self.parent_node_name), child=self.clean_name(self.child_node_name),
                   relationship=self.rel_type,
                   parameters=parameters_string)
        return clause

    def render_event(self, event_attr, event_text):
        event_date = self.__dict__.get(event_attr, None)

        if event_date is None:
            return None

        month_look_up = {'JAN': 1,
                         'FEB': 2,
                         'MAR': 3,
                         'APR': 4,
                         'MAY': 5,
                         'JUN': 6,
                         'JUL': 7,
                         'AUG': 8,
                         'SEP': 9,
                         'OCT': 10,
                         'NOV': 11,
                         'DEC': 12
                         }

        event_split = event_date.split('-')

        return {'event': event_text,
                'day': int(event_split[0]),
                'month': month_look_up[event_split[1]],
                'year': int(event_split[2])
                }

    @property
    def events(self):
        events = [self.render_event('start_date', f'{self.parent_node_name} became {self.link} of {self.child_node_name}'),
                  self.render_event('end_date',
                                    f'{self.parent_node_name} stopped being a  {self.link} of {self.child_node_name}')
                  ]

        events = [event for event in events if event is not None]

        return events


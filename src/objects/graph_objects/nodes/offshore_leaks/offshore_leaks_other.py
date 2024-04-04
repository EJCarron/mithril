from .offshore_leaks_node import OffshoreLeaksNode
from .....scripts.OffshoreLeaks import offshore_leaks_api

class OffshoreLeaksOther(OffshoreLeaksNode):

    @property
    def events(self):
        events = [self.render_event(event_attr='incorporation_date', event_text=f'{self.name} was incorporated'),
                  self.render_event(event_attr='inactivation_date', event_text=f'{self.name} was made inactive'),
                  self.render_event(event_attr='struck_off_date', event_text=f'{self.name} was struck off')
                  ]

        events = [event for event in events if event is not None]

        return events
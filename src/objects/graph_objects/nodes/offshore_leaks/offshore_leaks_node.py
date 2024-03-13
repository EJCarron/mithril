from ..node import Node
from .....scripts.OffshoreLeaks import offshore_leaks_api


class OffshoreLeaksNode(Node):

    def __init__(self, **kwargs):
        super(OffshoreLeaksNode, self).__init__()
        self.node_id = 'ol_' + str(kwargs['db_node_id'])
        self.__dict__.update(kwargs)

    @classmethod
    def batch_init(cls, node_ids):
        raw_results = offshore_leaks_api.get_nodes(node_ids)

        ol_types = {ol_type.__name__: ol_type for ol_type in cls.__subclasses__()}

        nodes = [ol_types[raw_result['node_type']](**raw_result) for raw_result in raw_results]

        return nodes

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

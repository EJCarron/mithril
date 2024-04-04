from .electoral_commission_node import ElectoralCommissionNode
from src.scripts.uk_electoral_commission import electoral_commission_api


class ElectoralCommissionRegulatedEntity(ElectoralCommissionNode):
    def __init__(self, **kwargs):
        super(ElectoralCommissionRegulatedEntity, self).__init__(**kwargs)

    def render_unique_label(self):
        return self.name.replace(' ', '_') + '_' + self.node_id

    @classmethod
    def batch_init(cls, node_ids):
        raw_results = electoral_commission_api.get_regulated_entities(node_ids)

        nodes = [cls(**result) for result in raw_results]

        return nodes

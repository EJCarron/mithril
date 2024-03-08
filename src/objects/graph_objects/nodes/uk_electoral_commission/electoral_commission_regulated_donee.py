from .electoral_commission_node import ElectoralCommissionNode


class ElectoralCommissionRegulatedDonee(ElectoralCommissionNode):
    def __init__(self, **kwargs):
        super(ElectoralCommissionRegulatedDonee, self).__init__()
        self.__dict__.update(kwargs)

    def render_unique_label(self):
        return self.name.replace(' ', '_')

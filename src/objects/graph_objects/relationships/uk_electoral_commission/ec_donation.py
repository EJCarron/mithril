from ..relationship import Relationship


class ElectoralCommissionDonation(Relationship):
    @property
    def events(self):

        date_split = self.date_accepted.split('/')

        reason = f'a visit to {self.destination} {self.purpose_of_vist}' if self.donation_type == 'visit' else self.nature_of_donation

        events = [{'day': int(date_split[0]),
                            'month':int(date_split[1]),
                   'year': int(date_split[2]),
                   'event':f'{self.regulated_donee} received a donation of {self.value} from {self.donor} for {reason}'
                   }]

        return events

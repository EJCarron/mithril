from src.objects.graph_objects.relationships.companies_house.companies_house_appointment import CompaniesHouseAppointment
from .relationship import Relationship
from .offshore_leaks.offshore_leaks_relationship import OffshoreLeaksRelationship
from .same_as import SameAs
from .uk_electoral_commission.donation import Donation

relationship_str = Relationship
ch_appointment_str = CompaniesHouseAppointment.__name__
ol_relationship_str = OffshoreLeaksRelationship.__name__
same_as_str = SameAs.__name__
donation_str = Donation.__name__

relationship = Relationship
ch_appointment = CompaniesHouseAppointment
ol_relationship = OffshoreLeaksRelationship
same_as = SameAs
donation = Donation

relationship_dict = {relationship_str: relationship,
                     ch_appointment_str: ch_appointment,
                     ol_relationship_str: ol_relationship,
                     same_as_str: same_as,
                     donation_str : donation
                     }

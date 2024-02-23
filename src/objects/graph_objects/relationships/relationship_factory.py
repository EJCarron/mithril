from src.objects.graph_objects.relationships.companies_house.companies_house_appointment import CompaniesHouseAppointment
from .relationship import Relationship
from .offshore_leaks.offshore_leaks_relationship import OffshoreLeaksRelationship

relationship_str = Relationship
ch_appointment_str = CompaniesHouseAppointment.__name__
ol_relationship_str = OffshoreLeaksRelationship.__name__

relationship = Relationship
ch_appointment = CompaniesHouseAppointment
ol_relationship = OffshoreLeaksRelationship

relationship_dict = {relationship_str: relationship,
                     ch_appointment_str: ch_appointment,
                     ol_relationship_str: ol_relationship
                     }

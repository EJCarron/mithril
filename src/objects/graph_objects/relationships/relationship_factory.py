from .companies_house_appointment import CompaniesHouseAppointment
from .relationship import Relationship

relationship_str = Relationship
ch_appointment_str = CompaniesHouseAppointment.__name__

relationship = Relationship
ch_appointment = CompaniesHouseAppointment

relationship_dict = {relationship_str: relationship,
                     ch_appointment_str: ch_appointment}

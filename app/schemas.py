
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models import AppointmentStatus


class PatientCreate(BaseModel):
    full_name:str
    date_of_birth:date
    phone:str | None = None

class PatientUptate(BaseModel):
    full_name:str|None = None
    date_of_birth:date |None = None
    phone:str|None = None

class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    full_name:str
    date_of_birth:date
    phone:str|None
    created_at:datetime

class AppointmentCreate(BaseModel):

    patient_id:int
    scheduled_at:datetime
    reason:str|None = None

class AppointmentOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id:int
    patient_id:int
    scheduled_at:datetime
    reason:str|None
    status:AppointmentStatus
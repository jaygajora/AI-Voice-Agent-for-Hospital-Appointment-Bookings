# Step 1: Import Database Objects
from database import init_db, Appointment, get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
import datetime as dt
import uvicorn

init_db()

# Step 2: Create FastAPI applications and pseudo code for endpoints
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

from pydantic import BaseModel

# Step 3: Create Data Contracts (DTOs) using Pydantic Models
class AppointmentRequest(BaseModel):
    patient_name : str
    reason : str
    start_time : dt.datetime

class AppointmentResponse(BaseModel):
    id : int
    patient_name : str
    reason : str | None
    start_time : dt.datetime
    cancelled : bool
    created_at : dt.datetime

class CancelAppointmentRequest(BaseModel):
    patient_name : str
    date: dt.date

class CancelAppointmentResponse(BaseModel):
    cancelled_count : int

class ListAppointmentsRequest(BaseModel):
    date: dt.date

class ListAppointmentsResponse(BaseModel):
    appointment_count: int 


# Endpoints:
    # scedule-appointment

    # cancel-appointment

    # check-availibility (of doctor)


@app.post("/schedule_appointment")
def schedule_appointment(request : AppointmentRequest, db: Session = Depends(get_db)):
    new_appointment = Appointment(
        patient_name = request.patient_name,
        reason = request.reason,
        start_time = request.start_time
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)   # the id of the entry gets stored/added to the "new_appointment" obj

    new_appointment_return_response = AppointmentResponse(
        id = new_appointment.id,
        patient_name = new_appointment.patient_name,
        reason = new_appointment.reason,
        start_time = new_appointment.start_time,
        cancelled = new_appointment.cancelled,
        created_at = new_appointment.created_at
    )

    return new_appointment_return_response


@app.post("/cancel_appointment")
def cancel_appointment(request : CancelAppointmentRequest, db: Session = Depends(get_db)):
    
    start_dt = dt.datetime.combine(request.date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)

    result = db.execute(
        select(Appointment)
        .where(Appointment.patient_name == request.patient_name)
        .where(Appointment.start_time >= start_dt)
        .where(Appointment.start_time < end_dt)  
        .where(Appointment.cancelled == False)
    )

    appointments = result.scalars().all()

    if not appointments:
        raise HTTPException(status_code=404, detail="No matching appointment found in our database")
    
    for appointment in appointments:
        appointment.cancelled = True

    db.commit()

    cancel_appointment_response = CancelAppointmentResponse(
        cancelled_count = len(appointments)
    )
     
    return cancel_appointment_response


@app.post("/list_appointments")
def list_appointment(request : ListAppointmentsRequest, db: Session = Depends(get_db)):
    
    start_dt = dt.datetime.combine(request.date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)

    result = db.execute(
        select(Appointment)
        .where(Appointment.cancelled == False)
        .where(Appointment.start_time >= start_dt)
        .where(Appointment.start_time < end_dt)
        .order_by(Appointment.start_time.asc())
    )

    booked_appointments = []

    for appointment in result.scalars():

        appointment_obj = AppointmentResponse(
            id = appointment.id,
            patient_name = appointment.patient_name,
            reason = appointment.reason,
            start_time = appointment.start_time,
            cancelled = appointment.cancelled,
            created_at = appointment.created_at
        )

        booked_appointments.append(appointment_obj)
    
    return booked_appointments



if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=4444, reload=True)



# Step 4: Streamlit dashboard testing (only for testing)
import streamlit as st
import datetime as dt
import requests
import time

st.title("Hospital Appointment Booking Portal")
base_url = st.text_input("Backend URL", "http://localhost:4444").rstrip("/")
# base_url = "http://localhost:4444"

st.subheader("Schedule Appointment")

patient_name = st.text_input("Patient Name")
reason = st.text_input("Reason for appointment")
start_date = st.date_input("Date", value=dt.date.today() + dt.timedelta(days=1))
start_time = st.time_input("Time", value=dt.time(9, 0))

if st.button("Schedule Appointment"):
    start_dt = dt.datetime.combine(start_date, start_time)

    payload = {
        "patient_name": patient_name.strip(),
        "reason": reason.strip() or None,
        "start_time": start_dt.isoformat(), 
    }

    try:
        response = requests.post(f"{base_url}/schedule_appointment", json=payload, timeout=10)
        response.raise_for_status()
        st.success("Appointment Scheduled")
    except requests.RequestException as ex:
        st.error(f"Schedule failed: {ex}")

st.divider()
st.subheader("Cancel Appointment")

cancel_name = st.text_input("Patient name to cancel", key="cancel_name")
cancel_date = st.date_input("Date to cancel", key="cancel_date", value=dt.date.today())

if st.button("Cancel Appointment"):
    payload = {
        "patient_name": cancel_name.strip(),
        "date": cancel_date.isoformat()
    }

    try:
        response = requests.post(f"{base_url}/cancel_appointment", json=payload, timeout=10)
        response.raise_for_status()
        data = response.json() if response.content else {}
        st.success(f"Cancelled count: {data.get('cancelled_count', 0)}")
        # st.toast("Appointment cancelled successfully!", icon="✅")
        time.sleep(2)
        st.rerun()
    except requests.HTTPError:
        st.error(response.text)
    except requests.RequestException as ex:
        st.error(f"Cancel failed: {ex}")



st.divider()
st.subheader("Check Scheduled Appointments")

appointment_date = st.date_input("Date to check appointments", key="check_appointment_date", value=dt.date.today())

if st.button("Check Appointment"):
    payload = {
        "date": appointment_date.isoformat()
    }

    try:
        response = requests.post(f"{base_url}/list_appointments", json=payload, timeout=10)
        response.raise_for_status()

        if len(response.json()) == 0:
            st.error(f"No appointments found for {appointment_date}")
        else:
            st.dataframe(response.json(), use_container_width=True, hide_index=True)
    except requests.RequestException as ex:
        st.warning(f"Could not load appointments: {ex}")


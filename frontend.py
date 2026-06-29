import streamlit as st
import datetime as dt
import requests
st.title("Hospital Appointment Booking Portal")
# base_url = st.text_input("Backend URL", "http://localhost:4444").rstrip("/")

st.subheader("Schedule")

patient_name = st.text_input("Patient Name")
reason = st.text_input("Reason for appointment")
start_date = st.date_input("Date", value=dt.date.today() + dt.timedelta(days=1))
start_time = st.time_input("Time", value=dt.time(9, 0))

if st.button("Schedule"):
    start_dt = dt.datetime.combine(start_date, start_time)

    payload = {
        "patient_name": patient_name.strip(),
        "reason": reason.strip() or None,
        "start_time": start_dt.isoformat(), 
    }

    try:
        response = requests.post(f"{base_url}/schedule_appointment", json=payload, timeout=10)
        response.raise_for_status()
        st.success("Scheduled Appointment")
    except requests.RequestException as ex:
        st.error(f"Schedule failed: {ex}")

st.divider()
st.subheader("Cancel")

cancel_name = st.text_input("Patient name to cancel", key="cancel_name")
cancel_date = st.date_input("Date to cancel", key="cancel_date", value=dt.date.today())

if st.button("Cancel"):
    payload = {
        "patient_name": cancel_name.strip(),
        "date": cancel_date.isoformat()
    }

    try:
        response = requests.post(f"{base_url}/cancel_appointment", json=payload, timeout=10)
        response.raise_for_status()
        data = response.json() if response.content else {}
        st.success(f"Canceled count: {data.get('cancelled_count', 0)}")
        st.rerun()
    except requests.HTTPError:
        st.error(response.text)
    except requests.RequestException as ex:
        st.error(f"Cancel failed: {ex}")


# st.divider()
# st.subheader("Scheduled?")

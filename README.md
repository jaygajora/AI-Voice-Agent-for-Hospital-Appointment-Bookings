# AI Voice Agent for Hospital Appointment Bookings

An AI-powered voice assistant that enables patients to book, view, update, and cancel hospital appointments using natural voice conversations. The application integrates **Vapi** for voice interactions, **FastAPI** for backend APIs, **Streamlit** for the frontend interface, **SQLite** for data storage, and **Ngrok** to expose the local backend for Vapi during development.

---

## Features

- 🎙️ Voice-based hospital appointment booking
- 📅 Schedule new appointments
- ✏️ Update existing appointments
- ❌ Cancel appointments
- 📋 View appointment details
- 🤖 AI-powered conversational interface using Vapi
- 💾 SQLite database for appointment storage
- 🌐 Public API access during development using Ngrok

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| FastAPI | Backend REST API |
| Streamlit | Frontend UI |
| SQLite | Database |
| Vapi | AI Voice Assistant |
| Ngrok | Expose local backend to the internet |

---

## Project Structure

```text
AI-Voice-Agent-for-Hospital-Appointment-Bookings/
│
├── backend.py          # FastAPI backend APIs
├── frontend.py         # Streamlit frontend
├── database.py         # Database operations
├── pyproject.toml      # Project dependencies
├── uv.lock             # Dependency lock file
└── README.md
```

---

## System Architecture

```text
                  +----------------------+
                  |      User Voice      |
                  +----------+-----------+
                             |
                             ▼
                  +----------------------+
                  |   Vapi Voice Agent   |
                  +----------+-----------+
                             |
                             ▼
                  +----------------------+
                  |     Ngrok Tunnel     |
                  +----------+-----------+
                             |
                             ▼
                  +----------------------+
                  | FastAPI Backend      |
                  | (localhost:4444)     |
                  +----------+-----------+
                             |
                             ▼
                  +----------------------+
                  | SQLite Database      |
                  +----------------------+
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/jaygajora/AI-Voice-Agent-for-Hospital-Appointment-Bookings.git

cd AI-Voice-Agent-for-Hospital-Appointment-Bookings
```

---

## 2. Install Dependencies

Using uv

```bash
uv sync
```

Or using pip

```bash
pip install -r requirements.txt
```

---

## 3. Start the FastAPI Backend

```bash
python backend.py
```

The backend runs on:

```
http://localhost:4444
```

---

## 4. Start the Streamlit Frontend

```bash
streamlit run frontend.py
```

---

# Ngrok Integration

The FastAPI backend runs locally on **localhost:4444**. Since **Vapi** cannot directly access APIs hosted on localhost, **Ngrok** is used to expose the backend over the internet.

## Step 1

Start the backend

```bash
python backend.py
```

---

## Step 2

Expose port **4444**

```bash
ngrok http 4444
```

Ngrok generates a public HTTPS URL similar to:

```
https://abc123.ngrok-free.app
```

---

## Step 3

Copy the generated HTTPS URL.

Example

```
https://abc123.ngrok-free.app
```

---

## Step 4

Open your **Vapi Dashboard**.

Navigate to your assistant's **Tools** section and configure each API endpoint using the Ngrok URL.

Example

Instead of

```
http://localhost:4444/book_appointment
```

Use

```
https://abc123.ngrok-free.app/book_appointment
```

Do the same for all API endpoints used by the voice assistant.

---

## Request Flow

```text
Patient
   │
   ▼
Vapi Voice Agent
   │
   ▼
Ngrok Public URL
   │
   ▼
FastAPI Backend (localhost:4444)
   │
   ▼
SQLite Database
   │
   ▼
Backend Response
   │
   ▼
Vapi Voice Agent
   │
   ▼
Patient
```

---

## Why Ngrok?

- Allows Vapi to access a backend running on localhost.
- Eliminates the need to deploy the backend during development.
- Securely tunnels HTTPS requests to the local FastAPI server.
- Makes local testing simple and efficient.

> **Note:** If you are using the free version of Ngrok, the public URL changes every time you restart the tunnel. Update the API endpoint URLs in the Vapi **Tools** configuration whenever a new Ngrok URL is generated.

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/book_appointment` | Book a new appointment |
| GET | `/appointments` | View appointments |
| PUT | `/update_appointment` | Update appointment details |
| DELETE | `/cancel_appointment` | Cancel an appointment |

---

# Workflow

1. User speaks with the AI Voice Agent.
2. Vapi understands the user's intent.
3. Vapi invokes the configured tool.
4. The request is sent to the Ngrok public URL.
5. Ngrok forwards the request to the FastAPI backend.
6. FastAPI processes the request.
7. Appointment data is stored or retrieved from SQLite.
8. The response is returned to Vapi.
9. Vapi responds naturally to the user.

---

# Future Improvements

- Google Calendar integration
- SMS/Email appointment reminders
- Multi-hospital support
- Doctor availability management
- Authentication for patients and staff
- Cloud deployment (AWS/GCP/Azure)

---

# Author

**Jay Dinesh Gajora**

GitHub: https://github.com/jaygajora

LinkedIn: https://www.linkedin.com/in/jaygajora/

---

# License

This project is intended for educational and learning purposes.

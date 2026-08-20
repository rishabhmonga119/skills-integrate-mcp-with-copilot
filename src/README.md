# Mergington High School Activities API

A FastAPI application that allows students to view extracurricular activities and teachers to manage registrations.

## Features

- View all available extracurricular activities
- Log in as a teacher
- Register and unregister students as an authenticated teacher

## Getting Started

1. Install the dependencies:

   ```
   pip install -r ../requirements.txt
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - Application: http://localhost:8000
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

The local teacher account is `teacher` with password `mergington2026`. Teacher credentials are stored in `teachers.json`. Set `TEACHERS_FILE` to use a different credential file and set a strong `SESSION_SECRET` outside local development. Set `SESSION_COOKIE_HTTPS_ONLY=true` when serving the application over HTTPS.

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/auth/status`                                                    | Get the current teacher login status                                |
| POST   | `/auth/login`                                                     | Log in with a teacher username and password                          |
| POST   | `/auth/logout`                                                    | Log out the current teacher                                         |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Register a student (teacher only)                                   |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher only)                              |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

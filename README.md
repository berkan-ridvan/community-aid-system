# Community Aid System

This project is a community assistance system that bridges the gap between residents and service providers.

## Features

- User Roles:
  - Service Requester (Resident)
  - Service Provider
- Service Requests:
  - Creation and Management
  - Search and Filtering
  - Bidding and Acceptance
- Messaging System
- Notifications
- Profile Management

## Installation

1. Install Python 3.8 or higher
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create the database:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Visit `http://127.0.0.1:8000` in your browser
2. Register or log in
3. Create service requests or bid on existing ones

## Technologies

- Django 5.2
- Bootstrap 5
- PostgreSQL
- Pillow (Image processing)
- Django Channels (Real-time messaging)
- Django Notifications (Notification system)

## License

MIT 
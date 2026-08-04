# SecureHome 

A full-stack real estate marketplace and property management system built 
with Django, Celery, Redis, PostgreSQL, and Tailwind CSS.

🔗 [Live Demo](https://securehome-kxch.onrender.com/)

---

## Overview

SecureHome streamlines property listing, house hunting, and property 
management in one platform. Landlords can list and manage properties; 
buyers and renters can search and filter listings. Background jobs 
(notifications, scheduling) run asynchronously via Celery and Redis, 
keeping response times fast under load.

## Features

- Property listing and search with filtering
- Landlord and tenant dashboards
- Async background task processing with Celery and Redis
- Database query optimisation with Django ORM and PostgreSQL
- Responsive UI built with Tailwind CSS
- Production deployment on Render with Procfile-based process management

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python, Django                    |
| Task Queue  | Celery, Redis                     |
| Database    | PostgreSQL                        |
| Frontend    | HTML, Tailwind CSS, JavaScript    |
| Deployment  | Render                            |

## Getting Started

### Prerequisites
- Python 3.x
- Redis server running locally
- PostgreSQL database

### Installation

```bash
git clone https://github.com/GreatFi/secureHome.git
cd secureHome
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

Add these variables
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DJANGO_SECRET_KEY=
Debug = True
MY_POSTGRES_PASSWORD = 
RESEND_API_KEY = 
CLOUDINARY_URL=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET= YOUR_CLOUDINARY_API_SECRET
DATABASE_URL =

### Run the app

```bash
python manage.py migrate
python manage.py runserver
```

In a separate terminal, start the Celery worker:

```bash
celery -A secureHome worker --loglevel=info --pool=solo
```

## Architecture Decisions

- **Celery + Redis** for async task processing — decouples background 
  jobs from the HTTP request cycle to maintain fast response times
- **PostgreSQL** with Django ORM for relational property and user data, 
  with query optimisation for improved load times
- **Double process deployment on Render** via Procfile — web server and 
  Celery worker run as separate processes

## Screenshots

HeroSection
-

<img width="1894" height="869" alt="image" src="https://github.com/user-attachments/assets/b889917b-812e-4953-b2d6-5a661e2cb34d" />

Landlord Dashboard
-

<img width="1900" height="846" alt="image" src="https://github.com/user-attachments/assets/aedc81b7-46b3-47ca-885b-caee1e96fa94" />


## Known Issues

- Live demo may experience downtime due to Render's free tier database 
  expiry policy. Screenshots will be added here for reference.
  
- Email Verification

  This project uses Resend for transactional email. During development, Resend restricts sending to the domain you've verified — emails to public providers          (Gmail, Outlook, Yahoo, etc.) will not be delivered unless your account has been approved for broader sending.
  
  What this means:
  
  Email verification will only work for addresses on your verified domain (e.g., you@yourdomain.com)
  Testing with personal email addresses (e.g., gmail.com) requires Resend account approval

Workarounds during development:

Use an address on your verified domain for testing
Check Resend's dashboard logs to confirm emails are being sent/blocked
Apply for production access in the Resend dashboard to lift this restriction

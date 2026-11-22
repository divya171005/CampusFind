# CampusFind – Campus Lost & Found Portal

A campus community web application where students can publish lost/found item reports, search listings, contact the poster, and mark an item as resolved.

## Features
- Create Lost and Found listings
- Search by title, description, or location
- Filter by Lost/Found type and category
- Contact poster through email link
- Mark a listing as resolved
- Optional MongoDB Atlas persistence
- In-memory demo mode if MongoDB is not configured

## Run locally (Windows PowerShell)
1. Open this folder in VS Code.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\Activate.ps1`
4. Install packages: `python -m pip install -r requirements.txt`
5. Copy `.env.example` to `.env`. MongoDB is optional for a local demo.
6. Run: `uvicorn main:app --reload`
7. Visit `http://127.0.0.1:8000`.

If PowerShell blocks activation, run:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
Then activate again.

## Docker
Build: `docker build -t campusfind:latest .`
Run: `docker run -p 8000:8000 campusfind:latest`

For persistent storage, configure `MONGODB_URI` and `MONGODB_DATABASE` in `.env` and run with:
`docker run --env-file .env -p 8000:8000 campusfind:latest`

## API endpoints
- `GET /api/health`
- `GET /api/items`
- `POST /api/items`
- `PATCH /api/items/{item_id}/resolve`

## Important limitations for this academic starter
- This is a demonstration MVP, not a production-ready campus service.
- There is no authentication or authorization yet. Anyone who can access the site can post listings or mark them resolved.
- Contact email is displayed to visitors through a mailto link.
- Before real campus deployment, add student authentication, moderation, abuse reporting, input rate limits, and ownership checks for resolving listings.
- Without MongoDB configured, records are stored in memory and disappear when the server restarts.

# NextZen Events — Deployable starter

Responsive event-management web app built with Flask + SQLite.

## Included features
- Event discovery with search, city and category filters
- Logged-in users can list events
- Vendor directory with categories, cities, sample prices and ratings
- Vendor booking requests and request tracking
- Account registration/login with hashed passwords
- Admin dashboard to update booking request status
- Responsive layout and `/health` endpoint
- Sample event and vendor data created automatically

## Run locally (Windows)
1. Install Python 3.10+.
2. Extract the ZIP and open the folder in VS Code/Terminal.
3. Run:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```
4. Open http://127.0.0.1:5000

## Deploy on Render
1. Push the extracted files to a new GitHub repository.
2. In Render choose **New + → Blueprint** and connect the repository.
3. Render reads `render.yaml`; deploy and open the generated URL.
4. Keep the persistent disk enabled for SQLite data.

Manual settings: build command `pip install -r requirements.txt`; start command `gunicorn app:app`. Set `SECRET_KEY` to a long random secret.

## Demo admin
Email: `admin@nextzen.local`  
Password: `ChangeMe123!`

Change the demo credentials before public launch.

## Routes
`/` events · `/events/new` create event · `/vendors` vendor discovery · `/vendors/<id>/book` booking request · `/my-bookings` request tracking · `/register` · `/login` · `/admin` · `/health`

## Production notes
Sample vendors, ratings, phone numbers and events are demonstration data; replace them with verified information. Payments, email/SMS notifications, image uploads, AI chatbot, digital contracts and native mobile apps are not integrated. SQLite is suitable for a demo/small single-instance deployment; consider managed PostgreSQL for larger production use.

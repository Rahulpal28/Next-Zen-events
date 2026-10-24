# 🎉 NextZen Events – Smart Event Management Platform

**NextZen Events** is a modern event management platform designed to simplify event planning, vendor discovery, and booking management. It helps users discover events and find suitable vendors based on location, category, and budget.

## 🚀 Features

- 🔍 **Event Discovery:** Search and filter events by city and category.
- 🎪 **Vendor Directory:** Explore event vendors, services, prices, and ratings.
- 📅 **Booking Management:** Submit vendor booking requests and track their status.
- 🔐 **User Authentication:** Secure registration and login with password hashing.
- 🛠️ **Admin Dashboard:** Manage booking requests and update booking statuses.
- 📝 **Event Listing:** Registered users can publish their own events.
- 📱 **Responsive Design:** User-friendly interface for desktop and mobile devices.
- 🗄️ **Database Integration:** SQLite database for storing users, events, vendors, and bookings.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (where applicable)
- **Database:** SQLite
- **Deployment:** Gunicorn, Render
- **Version Control:** Git and GitHub

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your actual GitHub details.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open your browser and visit:

`http://127.0.0.1:5000`

## 🌐 Deployment

The project includes a `render.yaml` configuration for deployment on Render.

1. Push the project files to GitHub.
2. Open [Render](https://render.com/

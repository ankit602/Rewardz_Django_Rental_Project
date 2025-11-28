# Student Book Rental System (Django)

## 📌 Overview
A complete student rental system where:
- Admin can start a rental
- Admin can extend rental & auto-calculate fees after free 30 days
- Dashboard shows all rentals with recommendations
- Extra Credit:
  ✔ Unit Tests  
  ✔ Recommendations Engine  
  ✔ Reports & Analytics Page  
  ✔ Improved UI

---

## 🚀 How to Run the Project

### 1. Clone the Repository
git clone <your-private-repo-url>
cd rewardz_project


### 2. Create Virtual Environment

python -m venv venv

### 3. Activate Virtual Environment
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

### 4. Install Dependencies
pip install -r requirements.txt

### 5. Run Migrations
python manage.py makemigrations
python manage.py migrate

### 6. Start Server
python manage.py runserver

### 7. Open in Browser  
Visit:

http://127.0.0.1:8000/dashboard/

## 🧪 Running Unit Tests

python manage.py test

---
## 📊 Reports Page
Visit:
http://127.0.0.1:8000/reports/

---

## ✔ Admin Login (Optional)
python manage.py createsuperuser
---
## 👨‍💻 Tech Stack
- Django 
- SQLite
- Bootstrap UI
- OpenLibrary API

---
## 👤 Author
Ankit Giri
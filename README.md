# Medicine Finder

A web application that helps users locate medicines at nearby pharmacies. Pharmacists can manage their inventory in real-time, and users can search for any medicine to instantly see which pharmacies have it in stock and in what quantity.

## Project Description

Medicine Finder connects two types of users — patients/buyers and pharmacists — on a single platform.

- Pharmacists register with their pharmacy's full address, then manage their medicine inventory by adding, editing, or removing stock.
- Users can register, sign in, and search for any medicine by name. The results show a list of pharmacies that carry it, along with available stock and the pharmacy's location.

The app supports role-based authentication — each account is either a user or a pharmacy, and the dashboard experience is tailored accordingly. Pharmacy address information is collected at sign-up, and sign-in/sign-out are fully supported.

Tech Stack: Python, Flask, SQLAlchemy, SQLite, Jinja2, HTML/CSS/JS

---

## Steps to Run the Project

Prerequisites: Python 3.8+ must be installed on your machine.

### 1. Clone the Repository

```bash
git clone <your-github-repo-link>
cd py-project-main/medicine-finder
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python backend/app.py
```

### 5. Open in Browser

Visit: http://localhost:5000

The SQLite database (medicine.db) is created automatically on first run. No manual database setup is needed.

Optional: To pre-populate the database with sample data, run:

```bash
python python/seed_data.py
```

---

## Team Members and Contributions

### Arham

- Inventory Management UI (inventory.html) — Built the pharmacist's inventory table view, displaying all medicines with stock levels and edit/delete actions.
- User Dashboard (user/dashboard.html) — Designed the landing page users see after logging in, with navigation to the search feature.
- Search Results Page (results.html) — Created the results display that lists matching pharmacies, their locations, and available medicine quantities.
- App Configuration (config.py) — Set up the Flask configuration class, including the secret key and SQLAlchemy database URI.
- Database Initialization (database.py) — Established the SQLAlchemy database object used across the app.
- Medicine Search Logic (routes/medicine.py) — Implemented the backend search query that looks up medicines across all pharmacy inventories, filtering by availability and sorting by stock.

### Vansh

- Medicine Search Page (search.html) — Built the user-facing search form where users enter a medicine name to begin their lookup.
- Base Template (base.html) — Created the shared HTML layout (navbar, flash messages, footer) inherited by all other pages in the app.
- Home / Landing Page (index.html) — Designed the application's welcome page that greets visitors and directs them to register or log in.
- Form Definitions (forms.py) — Defined Flask-WTF form classes used for input handling and validation.
- Database Models (models.py) — Architected the four core data models: User, Pharmacy, Medicine, and Inventory, including all relationships and foreign keys.
- Pharmacy Routes (routes/pharmacy.py) — Developed all pharmacist-facing routes: dashboard overview, adding medicines, editing quantities, and deleting stock entries.
- User Routes (routes/user.py) — Built the user dashboard and search results routes that render data for the patient-side of the app.

### Moksh

- Application Entry Point (app.py) — Assembled the main Flask app, registered all blueprints, configured folder paths, and handled database migrations for new columns on startup.
- Authentication System (routes/auth.py) — Implemented the full auth flow: registration with role selection and location capture, login with role-based redirects, and logout with session clearing.
- Login Page (templates/auth/login.html) — Built the sign-in form template.
- Registration Page (templates/auth/register.html) — Created the registration form, including conditional location fields that appear for pharmacist accounts.
- Add/Edit Medicine Form (templates/pharmacy/add_medicine.html) — Developed the form pharmacists use to add new medicines or update existing ones.
- Pharmacy Dashboard (templates/pharmacy/dashboard.html) — Built the pharmacist's overview panel showing total medicine count and low-stock alerts.
- Styling (static/css/style.css) — Authored the complete CSS stylesheet used across all pages.
- Frontend Interactivity (static/js/script.js) — Wrote the JavaScript for dynamic UI behaviour and client-side interactions.
- Seed Data Script (python/seed_data.py) — Created the script to populate the database with sample pharmacies, medicines, and inventory for testing.
- Dependencies File (requirements.txt) — Maintained the list of Python packages required to run the project.

---

## Project Demo Video

Watch the demo here: https://drive.google.com/file/d/164ZymEAA7MVEc-L4fykrZIHHRgWZ9Swh/view?usp=sharing

---


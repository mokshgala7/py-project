import os
import sys
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
	sys.path.insert(0, BACKEND_DIR)
from app import app
from database import db
from models import Inventory, Medicine, Pharmacy, User
def run_seed():
	with app.app_context():
		db.create_all()
		Inventory.query.delete()
		Pharmacy.query.delete()
		Medicine.query.delete()
		User.query.delete()
		db.session.commit()
		user_a = User(name="Asha Kumar", email="user1@medfind.com", password="user123", role="user")
		user_b = User(name="Rohan Patel", email="user2@medfind.com", password="user123", role="user")
		pharmacy_u1 = User(name="CityCare", email="pharmacy1@medfind.com", password="pharma123", role="pharmacy")
		pharmacy_u2 = User(name="HealthPlus", email="pharmacy2@medfind.com", password="pharma123", role="pharmacy")
		db.session.add_all([user_a, user_b, pharmacy_u1, pharmacy_u2])
		db.session.flush()
		p1 = Pharmacy(
			user_id=pharmacy_u1.id,
			pharmacy_name="CityCare Pharmacy",
			street="12 MG Road",
			city="Bengaluru",
			state="Karnataka",
			pincode="560001",
			country="India",
		)
		p2 = Pharmacy(
			user_id=pharmacy_u2.id,
			pharmacy_name="HealthPlus Pharmacy",
			street="45 Park Street",
			city="Kolkata",
			state="West Bengal",
			pincode="700016",
			country="India",
		)
		db.session.add_all([p1, p2])
		db.session.flush()
		m1 = Medicine(name="Paracetamol", manufacturer="analgesic")
		m2 = Medicine(name="Ibuprofen", manufacturer="analgesic")
		m3 = Medicine(name="Amoxicillin", manufacturer="antibiotic")
		m4 = Medicine(name="Metformin", manufacturer="antidiabetic")
		m5 = Medicine(name="Omeprazole", manufacturer="gastrointestinal")
		db.session.add_all([m1, m2, m3, m4, m5])
		db.session.flush()
		inventory_rows = [
			Inventory(pharmacy_id=p1.id, medicine_id=m1.id, quantity=120),
			Inventory(pharmacy_id=p1.id, medicine_id=m2.id, quantity=25),
			Inventory(pharmacy_id=p1.id, medicine_id=m3.id, quantity=8),
			Inventory(pharmacy_id=p2.id, medicine_id=m1.id, quantity=60),
			Inventory(pharmacy_id=p2.id, medicine_id=m4.id, quantity=40),
			Inventory(pharmacy_id=p2.id, medicine_id=m5.id, quantity=12),
		]
		db.session.add_all(inventory_rows)
		db.session.commit()
if __name__ == "__main__":
	run_seed()
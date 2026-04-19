from database import db


class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	role = db.Column(db.String(20), nullable=False)

	pharmacy = db.relationship("Pharmacy", back_populates="user", uselist=False)


class Pharmacy(db.Model):
	__tablename__ = "pharmacies"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	pharmacy_name = db.Column(db.String(150), nullable=False)
	street = db.Column(db.String(255), nullable=True)
	city = db.Column(db.String(120), nullable=True)
	state = db.Column(db.String(120), nullable=True)
	pincode = db.Column(db.String(20), nullable=True)
	country = db.Column(db.String(120), nullable=True)

	user = db.relationship("User", back_populates="pharmacy")
	inventories = db.relationship("Inventory", back_populates="pharmacy", cascade="all, delete-orphan")


class Medicine(db.Model):
	__tablename__ = "medicines"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), nullable=False, index=True)
	manufacturer = db.Column(db.String(150), nullable=True)

	inventories = db.relationship("Inventory", back_populates="medicine", cascade="all, delete-orphan")


class Inventory(db.Model):
	__tablename__ = "inventory"

	id = db.Column(db.Integer, primary_key=True)
	pharmacy_id = db.Column(db.Integer, db.ForeignKey("pharmacies.id"), nullable=False)
	medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)
	quantity = db.Column(db.Integer, nullable=False, default=0)

	pharmacy = db.relationship("Pharmacy", back_populates="inventories")
	medicine = db.relationship("Medicine", back_populates="inventories")

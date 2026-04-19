from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from database import db
from models import Inventory, Medicine, Pharmacy


pharmacy_bp = Blueprint("pharmacy", __name__)


def _current_pharmacy():
	user_id = session.get("user_id")
	if not user_id:
		return None
	return Pharmacy.query.filter_by(user_id=user_id).first()


@pharmacy_bp.route("/pharmacy")
def dashboard():
	pharmacy = _current_pharmacy()
	if not pharmacy:
		return redirect(url_for("auth.login"))

	items = Inventory.query.filter_by(pharmacy_id=pharmacy.id).all()
	medicine_count = len(items)
	low_stock_count = len([item for item in items if item.quantity < 10])

	return render_template(
		"pharmacy/dashboard.html",
		pharmacy={"name": pharmacy.pharmacy_name},
		medicine_count=medicine_count,
		low_stock_count=low_stock_count,
	)


@pharmacy_bp.route("/add-medicine", methods=["GET", "POST"])
def add_medicine():
	pharmacy = _current_pharmacy()
	if not pharmacy:
		return redirect(url_for("auth.login"))

	if request.method == "POST":
		medicine_name = (request.form.get("medicine_name") or "").strip()
		quantity = request.form.get("quantity", "0").strip()
		category = (request.form.get("category") or "").strip()

		if not medicine_name:
			flash("Medicine name is required.", "error")
			return render_template("pharmacy/add_medicine.html")

		try:
			qty_int = max(0, int(quantity))
		except ValueError:
			flash("Quantity must be a number.", "error")
			return render_template("pharmacy/add_medicine.html")

		medicine = Medicine.query.filter(db.func.lower(Medicine.name) == medicine_name.lower()).first()
		if not medicine:
			medicine = Medicine(name=medicine_name, manufacturer=category or None)
			db.session.add(medicine)
			db.session.flush()
		elif category and not medicine.manufacturer:
			medicine.manufacturer = category

		item = Inventory.query.filter_by(pharmacy_id=pharmacy.id, medicine_id=medicine.id).first()
		if item:
			item.quantity = qty_int
		else:
			item = Inventory(pharmacy_id=pharmacy.id, medicine_id=medicine.id, quantity=qty_int)
			db.session.add(item)

		db.session.commit()
		flash("Medicine saved to inventory.", "success")
		return redirect(url_for("pharmacy.inventory"))

	return render_template("pharmacy/add_medicine.html")


@pharmacy_bp.route("/inventory")
def inventory():
	pharmacy = _current_pharmacy()
	if not pharmacy:
		return redirect(url_for("auth.login"))

	items = (
		Inventory.query.join(Medicine, Inventory.medicine_id == Medicine.id)
		.filter(Inventory.pharmacy_id == pharmacy.id)
		.order_by(Medicine.name.asc())
		.all()
	)

	medicines = [
		{
			"id": item.id,
			"name": item.medicine.name,
			"category": item.medicine.manufacturer,
			"quantity": item.quantity,
		}
		for item in items
	]

	return render_template("pharmacy/inventory.html", medicines=medicines)


@pharmacy_bp.route("/edit-medicine/<int:id>", methods=["GET", "POST"])
def edit_medicine(id):
	pharmacy = _current_pharmacy()
	if not pharmacy:
		return redirect(url_for("auth.login"))

	item = Inventory.query.filter_by(id=id, pharmacy_id=pharmacy.id).first_or_404()

	if request.method == "POST":
		quantity = request.form.get("quantity", "0").strip()
		try:
			item.quantity = max(0, int(quantity))
			db.session.commit()
			flash("Inventory updated.", "success")
		except ValueError:
			flash("Quantity must be a number.", "error")
		return redirect(url_for("pharmacy.inventory"))

	return render_template("pharmacy/add_medicine.html")


@pharmacy_bp.route("/delete-medicine/<int:id>", methods=["POST"])
def delete_medicine(id):
	pharmacy = _current_pharmacy()
	if not pharmacy:
		return redirect(url_for("auth.login"))

	item = Inventory.query.filter_by(id=id, pharmacy_id=pharmacy.id).first_or_404()
	db.session.delete(item)
	db.session.commit()
	flash("Medicine removed from inventory.", "success")
	return redirect(url_for("pharmacy.inventory"))

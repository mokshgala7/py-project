from flask import Blueprint, redirect, request, url_for
from sqlalchemy import func

from models import Inventory, Medicine, Pharmacy


medicine_bp = Blueprint("medicine", __name__)


def _format_location(pharmacy):
	parts = [
		(pharmacy.street or "").strip(),
		(pharmacy.city or "").strip(),
		(pharmacy.state or "").strip(),
		(pharmacy.pincode or "").strip(),
		(pharmacy.country or "").strip(),
	]
	return ", ".join([part for part in parts if part])


def find_medicine_results(query_text):
	q = (query_text or "").strip()
	if not q:
		return []

	rows = (
		Inventory.query.join(Medicine, Inventory.medicine_id == Medicine.id)
		.join(Pharmacy, Inventory.pharmacy_id == Pharmacy.id)
		.filter(Inventory.quantity > 0)
		.filter(func.lower(Medicine.name).like(f"%{q.lower()}%"))
		.order_by(Inventory.quantity.desc(), Pharmacy.pharmacy_name.asc())
		.all()
	)

	return [
		{
			"pharmacy_name": row.pharmacy.pharmacy_name,
			"location": _format_location(row.pharmacy),
			"medicine_name": row.medicine.name,
			"quantity": row.quantity,
		}
		for row in rows
	]


@medicine_bp.route("/medicine/search", methods=["POST"])
def search_form_handler():
	q = (request.form.get("q") or "").strip()
	if q:
		return redirect(url_for("user.results", q=q))
	return redirect(url_for("user.search"))

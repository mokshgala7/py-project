from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from database import db
from models import Pharmacy, User


auth_bp = Blueprint("auth", __name__)


def _redirect_if_logged_in():
	if not session.get("user_id"):
		return None

	flash("You are already signed in. Please sign out first to switch account.", "error")
	if session.get("role") == "pharmacy":
		return redirect(url_for("pharmacy.dashboard"))
	return redirect(url_for("user.dashboard"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	blocked = _redirect_if_logged_in()
	if blocked:
		return blocked

	if request.method == "POST":
		name = (request.form.get("name") or "").strip()
		email = (request.form.get("email") or "").strip().lower()
		password = (request.form.get("password") or "").strip()
		role = (request.form.get("role") or "").strip().lower()
		street = (request.form.get("street") or "").strip()
		city = (request.form.get("city") or "").strip()
		state = (request.form.get("state") or "").strip()
		pincode = (request.form.get("pincode") or "").strip()
		country = (request.form.get("country") or "").strip()

		if not name or not email or not password or role not in {"user", "pharmacy"}:
			flash("Please fill all required fields.", "error")
			return render_template("auth/register.html")

		if role == "pharmacy" and (not street or not city or not state or not pincode):
			flash("Pharmacy accounts must include full store location details.", "error")
			return render_template("auth/register.html")

		existing_user = User.query.filter_by(email=email).first()
		if existing_user:
			flash("Email is already registered.", "error")
			return render_template("auth/register.html")

		user = User(name=name, email=email, password=password, role=role)
		db.session.add(user)
		db.session.flush()

		if role == "pharmacy":
			profile = Pharmacy(
				user_id=user.id,
				pharmacy_name=f"{name} Pharmacy",
				street=street,
				city=city,
				state=state,
				pincode=pincode,
				country=country or "India",
			)
			db.session.add(profile)

		db.session.commit()
		flash("Registration successful. Please sign in.", "success")
		return redirect(url_for("auth.login"))

	return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	blocked = _redirect_if_logged_in()
	if blocked:
		return blocked

	if request.method == "POST":
		email = (request.form.get("email") or "").strip().lower()
		password = (request.form.get("password") or "").strip()

		user = User.query.filter_by(email=email, password=password).first()
		if not user:
			flash("Invalid email or password.", "error")
			return render_template("auth/login.html")

		session["user_id"] = user.id
		session["role"] = user.role
		session["name"] = user.name

		if user.role == "pharmacy":
			profile = Pharmacy.query.filter_by(user_id=user.id).first()
			if not profile:
				db.session.add(
					Pharmacy(
						user_id=user.id,
						pharmacy_name=f"{user.name} Pharmacy",
						street="",
						city="",
						state="",
						pincode="",
						country="India",
					)
				)
				db.session.commit()
			return redirect(url_for("pharmacy.dashboard"))

		return redirect(url_for("user.dashboard"))

	return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
	session.clear()
	flash("Logged out successfully.", "success")
	return redirect(url_for("index"))

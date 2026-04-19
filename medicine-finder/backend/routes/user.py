from flask import Blueprint, render_template, request, session

from models import User
from routes.medicine import find_medicine_results


user_bp = Blueprint("user", __name__)


@user_bp.route("/dashboard")
def dashboard():
	user_id = session.get("user_id")
	current_user = User.query.get(user_id) if user_id else None
	return render_template("user/dashboard.html", current_user=current_user)


@user_bp.route("/search")
def search():
	return render_template("user/search.html")


@user_bp.route("/results")
def results():
	query = (request.args.get("q") or "").strip()
	results_data = find_medicine_results(query)
	return render_template("user/results.html", query=query, results=results_data)

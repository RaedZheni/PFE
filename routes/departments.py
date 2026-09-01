from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.department import Department
from app import db

departments = Blueprint("departments", __name__)

@departments.route("/departments")
@login_required
def index():
    all_departments = Department.query.all()
    return render_template("departments/index.html", departments=all_departments)

@departments.route("/departments/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        dept = Department(name=name, description=description)
        db.session.add(dept)
        db.session.commit()
        flash("Department created", "success")
        return redirect(url_for("departments.index"))
    return render_template("departments/create.html")

@departments.route("/departments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    dept = Department.query.get_or_404(id)
    if request.method == "POST":
        dept.name = request.form.get("name")
        dept.description = request.form.get("description")
        db.session.commit()
        flash("Department updated", "success")
        return redirect(url_for("departments.index"))
    return render_template("departments/edit.html", dept=dept)

@departments.route("/departments/delete/<int:id>")
@login_required
def delete(id):
    dept = Department.query.get_or_404(id)
    for emp in dept.employees:
        emp.department_id = None
    db.session.commit()
    db.session.delete(dept)
    db.session.commit()
    flash("Department deleted", "warning")
    return redirect(url_for("departments.index"))
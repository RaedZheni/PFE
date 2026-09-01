from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.employee import Employee
from models.department import Department
from app import db

employees = Blueprint("employees", __name__)

@employees.route("/employees")
@login_required
def index():
    all_employees = Employee.query.all()
    return render_template("employees/index.html", employees=all_employees)

@employees.route("/employees/create", methods=["GET", "POST"])
@login_required
def create():
    departments = Department.query.all()
    if request.method == "POST":
        emp = Employee(
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            role=request.form.get("role"),
            department_id=request.form.get("department_id")
        )
        db.session.add(emp)
        db.session.commit()
        flash("Employee created", "success")
        return redirect(url_for("employees.index"))
    return render_template("employees/create.html", departments=departments)

@employees.route("/employees/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    emp = Employee.query.get_or_404(id)
    departments = Department.query.all()
    if request.method == "POST":
        emp.first_name = request.form.get("first_name")
        emp.last_name = request.form.get("last_name")
        emp.email = request.form.get("email")
        emp.phone = request.form.get("phone")
        emp.role = request.form.get("role")
        emp.department_id = request.form.get("department_id")
        db.session.commit()
        flash("Employee updated", "success")
        return redirect(url_for("employees.index"))
    return render_template("employees/edit.html", emp=emp, departments=departments)

@employees.route("/employees/delete/<int:id>")
@login_required
def delete(id):
    emp = Employee.query.get_or_404(id)
    for task in emp.tasks:
        task.employee_id = None
    db.session.commit()
    db.session.delete(emp)
    db.session.commit()
    flash("Employee deleted", "warning")
    return redirect(url_for("employees.index"))
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.contract import Contract
from models.employee import Employee
from app import db
from datetime import datetime

contracts = Blueprint("contracts", __name__)

@contracts.route("/contracts")
@login_required
def index():
    all_contracts = Contract.query.all()
    return render_template("contracts/index.html", contracts=all_contracts)

@contracts.route("/contracts/create", methods=["GET", "POST"])
@login_required
def create():
    employees = Employee.query.all()
    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        if not employee_id:
            flash("Please select an employee", "danger")
            return render_template("contracts/create.html", employees=employees)
        end_date = request.form.get("end_date")
        contract = Contract(
            type=request.form.get("type"),
            start_date=datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date(),
            end_date=datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None,
            salary=request.form.get("salary"),
            employee_id=employee_id
        )
        db.session.add(contract)
        db.session.commit()
        flash("Contract created", "success")
        return redirect(url_for("contracts.index"))
    return render_template("contracts/create.html", employees=employees)

@contracts.route("/contracts/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    contract = Contract.query.get_or_404(id)
    employees = Employee.query.all()
    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        if not employee_id:
            flash("Please select an employee", "danger")
            return render_template("contracts/edit.html", contract=contract, employees=employees)
        end_date = request.form.get("end_date")
        contract.type = request.form.get("type")
        contract.start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date()
        contract.end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
        contract.salary = request.form.get("salary")
        contract.employee_id = employee_id
        db.session.commit()
        flash("Contract updated", "success")
        return redirect(url_for("contracts.index"))
    return render_template("contracts/edit.html", contract=contract, employees=employees)

@contracts.route("/contracts/delete/<int:id>")
@login_required
def delete(id):
    contract = Contract.query.get_or_404(id)
    db.session.delete(contract)
    db.session.commit()
    flash("Contract deleted", "warning")
    return redirect(url_for("contracts.index"))
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.employee import Employee
from models.contract import Contract
from models.project import Project
from models.department import Department

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
@login_required
def index():
    total_employees = Employee.query.count()
    total_departments = Department.query.count()
    total_projects = Project.query.count()
    active_contracts = len([c for c in Contract.query.all() if c.is_active])
    return render_template("dashboard.html",
        total_employees=total_employees,
        total_departments=total_departments,
        total_projects=total_projects,
        active_contracts=active_contracts
    )

@dashboard.route("/api/context")
@login_required
def context():
    employees = Employee.query.all()
    projects = Project.query.all()
    contracts = Contract.query.all()

    data = {
        "employees": [
            {
                "name": f"{e.first_name} {e.last_name}",
                "role": e.role,
                "department": e.department.name if e.department else None,
                "email": e.email
            } for e in employees
        ],
        "projects": [
            {
                "name": p.name,
                "status": p.status,
                "tasks": [
                    {
                        "title": t.title,
                        "status": t.status,
                        "assigned_to": f"{t.employee.first_name} {t.employee.last_name}" if t.employee else None
                    } for t in p.tasks
                ]
            } for p in projects
        ],
        "contracts": [
            {
                "employee": f"{c.employee.first_name} {c.employee.last_name}",
                "type": c.type,
                "active": c.is_active,
                "salary": c.salary
            } for c in contracts
        ]
    }
    return jsonify(data)
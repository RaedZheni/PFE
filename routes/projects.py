from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required
from models.project import Project
from models.task import Task
from models.employee import Employee
from app import db
from datetime import datetime

projects = Blueprint("projects", __name__)

@projects.route("/projects")
@login_required
def index():
    all_projects = Project.query.all()
    return render_template("projects/index.html", projects=all_projects)

@projects.route("/projects/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        project = Project(
            name=request.form.get("name"),
            description=request.form.get("description"),
            status=request.form.get("status", "active")
        )
        db.session.add(project)
        db.session.commit()
        flash("Project created", "success")
        return redirect(url_for("projects.index"))
    return render_template("projects/create.html")

@projects.route("/projects/delete/<int:id>")
@login_required
def delete(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted", "warning")
    return redirect(url_for("projects.index"))

@projects.route("/projects/<int:id>/kanban")
@login_required
def kanban(id):
    project = Project.query.get_or_404(id)
    employees = Employee.query.all()
    tasks = {
        "todo": Task.query.filter_by(project_id=id, status="todo").all(),
        "inprogress": Task.query.filter_by(project_id=id, status="inprogress").all(),
        "done": Task.query.filter_by(project_id=id, status="done").all(),
    }
    return render_template("projects/kanban.html", project=project, tasks=tasks, employees=employees)

@projects.route("/projects/task/create", methods=["POST"])
@login_required
def create_task():
    data = request.json
    due_date = data.get("due_date")
    task = Task(
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status", "todo"),
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None,
        project_id=data.get("project_id"),
        employee_id=data.get("employee_id") or None
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"success": True, "task_id": task.id})

@projects.route("/projects/task/update/<int:id>", methods=["POST"])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    task.status = data.get("status", task.status)
    db.session.commit()
    return jsonify({"success": True})

@projects.route("/projects/task/delete/<int:id>", methods=["POST"])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": True})
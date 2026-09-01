from extensions import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="todo")
    due_date = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id", ondelete="SET NULL"), nullable=True)
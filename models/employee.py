from extensions import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id", ondelete="SET NULL"), nullable=True)
    contracts = db.relationship("Contract", backref="employee", lazy=True, cascade="all, delete-orphan")
    tasks = db.relationship("Task", backref="employee", lazy=True)
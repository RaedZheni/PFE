from extensions import db
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="active")  # active, completed, on_hold
    tasks = db.relationship("Task", backref="project", lazy=True, cascade="all, delete-orphan")
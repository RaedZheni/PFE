from extensions import db
from datetime import date

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # CDI, CDD, Internship
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    salary = db.Column(db.Float)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    @property
    def is_active(self):
        if self.end_date is None:
            return True
        return self.end_date >= date.today()
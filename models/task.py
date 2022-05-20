from extensions import db
from datetime import datetime

class Task(db.Model):
    """model to store a task data"""

    id = db.Column(db.Integer, primary_key=True)
    """:type : int"""

    hours = db.Column(db.String(150), default="00:00")
    description = db.Column(db.String(200), nullable=False)
    situation = db.Column(db.String(150))
    """:type : str"""

    date_created = db.Column(db.DateTime, default=datetime.now)
    date_finished = db.Column(db.DateTime, default=datetime.now)
    date_initial = db.Column(db.DateTime, default=datetime.now)
    """:type : datetime"""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self):
        """override __repr__ method"""
        return f"Task: #{self.id}, content: {self.description}, content: {self.situation}, content: {self.date_finished}, content: {self.hours}, content: {self.category_id}, content: {self.user_id}"

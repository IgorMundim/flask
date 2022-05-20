from extensions import db

class User (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    """:type : int"""

    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    """:type : str"""
    
    task = db.relationship("Task", backref="user")

    def __repr__(self):
        """override __repr__ method"""
        return f"Task: #{self.id}, content: {self.name}, content: {self.password}"

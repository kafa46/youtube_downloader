from server  import db

class VisitData(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    url = db.Column(db.String(500), nullable=True)
from app import db

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)
    location = db.Column(db.String(50),nullable=False)
    date = db.Column(db.DateTime,nullable=False)

   

    
    def __init__(self, name, location, date):
        self.name = name
        self.location = location
        self.date = date

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'location': self.location,
            'date':self.date
        }
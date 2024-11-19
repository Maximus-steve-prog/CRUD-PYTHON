from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Role(db.Model):
    IdRole = db.Column(db.Integer, primary_key=True)
    LibRole = db.Column(db.String(255), nullable=False)

class User(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    IdRole = db.Column(db.Integer, db.ForeignKey('role.IdRole'))
    
    def to_dict(self):
            return {
            'id': self.Id,
            'name': self.name,
            'email': self.email,
            'image':self.image,
            'IdRole':self.IdRole
        }
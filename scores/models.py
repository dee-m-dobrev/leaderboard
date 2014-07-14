from scores import db

class User(db.Model):
    name = db.Column(db.String(64), index = True, primary_key = True)
    min = db.Column(db.Integer, index = True)
    sec = db.Column(db.Integer, index = True)
    time = db.Column(db.Integer, index = True)

    def __repr__(self):
        return self.name
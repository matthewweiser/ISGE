from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    horses = db.relationship('Horse', backref='owner', lazy='dynamic')

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    
    def __repr__(self):
        return '<User %r>' % (self.uname)

class Horse(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    experiment_id = db.Column(db.String(64))
    hname = db.Column(db.String(64))
    sire = db.Column(db.String(64))
    dam = db.Column(db.String(64))
    pc1 = db.Column(db.Float())
    pc2 = db.Column(db.Float())
    pc3 = db.Column(db.Float())
    pc4 = db.Column(db.Float())
    pc5 = db.Column(db.Float())
    pc6 = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.hname)        
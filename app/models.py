from extensions import db

class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(200))
  personal_id = db.Column(db.String(15))
  password = db.Column(db.String(200))
  email = db.Column(db.String(50))
  phone = db.Column(db.String(15))
  kind = db.Column(db.String(20))
  confirmed = db.Column(db.Boolean)

  def __repr__(self):
    return '<User {}>'.format(self.personal_id)

class Authors(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  book = db.Column(db.String(20), unique=True, nullable=False)
  country = db.Column(db.String(50), nullable=False)
  booker_prize = db.Column(db.Boolean)
  user_id = db.Column(db.Integer)
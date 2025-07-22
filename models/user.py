from appconfigs.db_conn import db


class User(db.Model):
    __tablename__ = 'user'  # Explicitly naming the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    profile_picture = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'
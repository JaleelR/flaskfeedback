from models import db, User
from app import app

db.drop_all()
db.create_all()

user1 = User(username = "Zenzone", password = "zen", email = "zenzone@gmail.com", first_name = "zen", last_name = "zone")
user2 = User(username = "money", password = "$", email = "money@gmail.com", first_name = "man", last_name = "money")

db.session.add_all([user1, user2])
db.session.commit()
from app.service.user_service import *


def saveAllToDB(data):
    db.session.add_all(data)
    db.session.commit()


def createUsers():
    try:
        register(username="ChefBesos", email="jeffbezos@gmail.com", lastName="Besos", firstName="Chef",
             password="Passwort123!")
        register(username="EronMisk", email="eronmisk@gmail.com", lastName="Misk", firstName="Eron",
                 password="Passwort123!")
        register(username="billyShorts", email="billgates@gmail.com", lastName="Gates", firstName="Jill I'm Single",
                 password="Passwort123!")
        register(username="Max", email="max@gmail.com", lastName="Mustermann", firstName="Max", password="Passwort123!")
        register(username="femu", email="demo@test.de", lastName="Muth", firstName="Ferdi", password="Test")
        print('added: users')
    except Exception as e:
        print(f"Following Error while running createUsers() from generate.py: \n{e}")

def generate():
    createUsers()



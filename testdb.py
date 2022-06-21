from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.TaskManager
myDb = client["quixJourn"]
mytbl = myDb["user_info"]

def createAcc():
    # form = pf.RegistrationForm()
#     global users
    username = "sansi"
    email = "sansi@gmail.com"
    password = "123"
    u_type = "poet"
    user = {'username': username, 'email': email, 'password': password, 'type': u_type}
    # db.tasks.insert_one(user)
    x = mytbl.insert_one(user)
    return x
print(createAcc())
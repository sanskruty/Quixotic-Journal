from flask import Flask,render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route("/")
def home_page():
    online_users = mongo1.db.users.find({"online": True})
    return render_template("index.html",online_users=online_users)

@app.route("/user/<username>")
def user_profile(username):
    user = mongo1.db.users.find_one_or_404({"_id": username})
    return render_template("user.html",user=user)
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_wtf import form
import requests
from pymongo import MongoClient
from pilotForm import RegistrationForm, LoginForm
import pilotPyttsx as au
import ttos as saveAu
import pilotRhymer as rhy
import pilotThesaurus as the
import defs
import pilotAutoc as ac
import datetime
# import make_prediction as mp

app = Flask(__name__)

app.config['SECRET_KEY'] = '9d1bab8becf05d4b9aee914a'
client = MongoClient('localhost:27017')
myDb = client["quixJourn"]
mytbl = myDb["user_info"]
mypoem = myDb["poem_tbl"]
myrec = myDb["poem_rec"]
mySub = myDb["sub_tbl"]
mynoti = myDb['noti_tbl']
mylast = myDb['last_tbl']

users = {}
u_email = ""
u_pass = ""
err = ""


# def Notifications(subList, loginTime, previouslyViewed):
#     for poet in subList:
#         recs = mypoem.find({'username': poet, 'datetime': {'$lte': previouslyViewed, '$gte': loginTime}})

@app.route('/writer', methods=['GET', 'POST'])
def writer():
    global users
    users = session['users']
    type = users['type']
    try:
        if session['flag'] is not None:
            flag = session['flag']
    except KeyError:
        flag = ""
    try:
        if session['text'] is not None:
            text = session['text']
    except KeyError:
        text = ""
    try:
        if session['fname'] is not None:
            fname = session['fname']
    except KeyError:
        fname = ""

    # au.playAudio("You can frame your poem here")
    return render_template('writer.html', text=text, fname=fname, type=type, flag=flag)


@app.route('/')
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    # au.playAudio("Welcome to quixotic journal")
    if request.method == "POST":
        checker = mytbl.find_one({'email': form.email.data, 'type': form.type.data})
        typeChek = mytbl.find_one({'username': form.username.data})
        if (checker is not None) or (typeChek is not None):
            au.playAudio("Email-id  or username is already in use, try registering again.")
            return redirect('register')
        user = {'username': form.username.data, 'email': form.email.data, 'password': form.password.data,
                'type': form.type.data}
        mytbl.insert_one(user)
        return redirect('login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global users
    formL = LoginForm()

    global u_email, u_pass
    if request.method == "POST":
        u_email = formL.email.data
        u_pass = formL.password.data
        u_type = formL.type.data
        users = user_log = mytbl.find_one({'email': u_email, 'password': u_pass, 'type': u_type})
        if user_log is None:
            global err
            err = "none"
            au.playAudio("Please check your email-id and password")
            return render_template('login.html', form=formL)
        else:
            session['users'] = {'username': users['username'], 'email': users['email'], 'password': users['password'],
                                'type': users['type']}
            session['epname'] = " "
            session['loginTime'] = datetime.datetime.utcnow()
            session['flag'] = ""
            au.playAudio("Login successful")
            if u_type == "poet":
                return redirect('writer')
            elif u_type == "reader":
                return redirect('writer')
    return render_template('login.html', form=formL)


@app.route('/', methods=['GET', 'POST'])
def listen():
    if request.method == 'POST':
        try:
            if request.form['poem'] and request.form['fileName'] is not None:
                text = request.form['poem']
                name = request.form['fileName']
        except KeyError:
            text = ""
            name = ""
        # keywords = request.form['keywords']
        btn = request.form['save']
        # type = users['type']
        users = session['users']
        type = users['type']
        session['text'] = text
        users = session['users']
        flag = session['flag']
        username = users['username']
        if btn == "reset":
            session['text'] = text = ""
            session['fname'] = fname = ""
            session['flag'] = flag = ""
            return render_template('writer.html', text=text, fname=fname, flag=flag)
        if btn == "play":
            if text == "":
                return render_template('writer.html', text=text)
            else:
                print("play")
                flag = au.playAudio(text)
                if flag == 0:
                    ring = "Please refresh the page"
                else:
                    ring = ""
            return render_template('writer.html', text=text, fname=name, type=type)
        elif btn == "file_save":
            if name != "" and text != "":
                if mypoem.find_one({'poem_name': name}):
                    mypoem.update_one({'poem_name': name}, {
                        "$set": {'poem': text, 'user': username, 'dateTime': datetime.datetime.utcnow(), 'draft': False}})
                    if mySub.find_one({'pid': users['username']}):
                        for user in mySub.find({'pid':username}):
                            mynoti.insert_one({'uid': user['uid'], 'poet': username, 'corp': poem_file})
                else:
                    poem_file = {"poem_name": name, "poem": text, "user": username,
                                 'dateTime': datetime.datetime.utcnow(), 'draft': False}
                    mypoem.insert_one(poem_file)
                    if mySub.find_one({'pid': users['username']}):
                        for user in mySub.find({'pid':username}):
                            mynoti.insert_one({'uid': user['uid'], 'poet': username, 'dateTime':datetime.datetime.utcnow(), 'corp': poem_file})
                # saveAu.saveAudio(text, name)
                ring = ""

            return render_template('writer.html', text=text, fname=name)
        elif btn == "draft":
            if name != "" and text != "":
                poem_file = {"poem_name": name, "poem": text, "user": username, 'dateTime': datetime.datetime.utcnow(),
                             'draft': True}
                mypoem.insert_one(poem_file)
            return render_template('writer.html', text=text, fname=name)
        elif btn == "sugg":
            text = text.strip()
            li = text.split("\n")
            lilen = len(li)
            wds = li[lilen - 1].split(" ")
            wdslen = len(wds)
            if wdslen > 2:
                fwd = wds[wdslen - 2]
                sl = wds[wdslen - 1]
                sugg = ac.autoc(fwd, sl[0])
            else:
                sugg = []
        return render_template('writer.html', text=text, fname=name, list=sugg, type=type, flag=flag)


@app.route('/search')
def search():
    # au.playAudio("You can search rhyming words, synonyms and definition here.")
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search_wd():
    word = request.form['search']
    listRhy = rhy.sRhy(word)
    listThe = the.sThe(word)
    listDef = defs.sDef(word)
    if listThe == 0 or listThe == '':
        listThe = ['Given word has no synonyms.']
    if listRhy == 0 or listRhy == '':
        listRhy = ['Given word has no Rhymers']
    if listDef == 0 or listDef == 'the cardinal number that is the sum of one and one and one':
        listDef = 'Given word has no definition'
    return render_template('search.html', listRhy=listRhy, listThe=listThe, listDef=listDef, word=word)


@app.route('/journals', methods=['GET', 'POST'])
def journals():
    x = ""
    global users
    users = session['users']
    type = users['type']
    username = users['username']
    poem = mypoem.find({'user': username})
    # poem['poem']="x"
    # mypoem.delete_one({'poem_name': 'myStory'})
    if request.method == 'POST':
        operation = request.form['operation']
        choice = operation.split(" ")
        for itr in range(1, len(choice)):
            x = x + choice[itr] + " "
        x = x.strip()
        if choice[0] == "del":
            delete = x
            mypoem.delete_one({'poem_name': delete})

        elif choice[0] == "edit":
            edit = x
            rec = mypoem.find_one({'poem_name': edit})
            text = rec["poem"]
            session["text"] = text
            session["fname"] = edit
            flag = session['flag']
            return render_template('writer.html', text=text, fname=edit, type=type, flag=flag)
        elif choice[0] == "play":
            play = x
            rec = mypoem.find_one({'poem_name': play})
            text = rec["poem"]
            au.playAudio(text)
        return render_template('journals.html', poems=poem)

    return render_template('journals.html', poems=poem)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = session['users']
    type = users['type']
    uname = users['username']
    session['viewTime'] = datetime.datetime.utcnow()
    # subList = {}
    subList = mySub.find({'uid': uname})
    x = mySub.find({'uid': uname})
    subCount = subList.count()
    # if subCount > 0:
    #     Notifications(subList, session['loginTime'])
    if request.method == "POST":
        operation = request.form['sub']
        choice = operation.split(" ")
        if choice[0] == "logout":
            session.pop('users', None)
            session.pop('text', None)
            session.pop('fname', None)
            return redirect('login')
        elif choice[0] == "view":
            if mylast.find_one({'uid': users['username']}):
                mylast.update_one({'uid': users['username']}, {'$set': {'lasttime': datetime.datetime.utcnow()}})
            else:
                mylast.insert_one({'uid': users['username'], 'lasttime': datetime.datetime.utcnow()})
            poem_corp = mypoem.find_one({'poem_name':choice[1]})
            poem = poem_corp['poem']
            return render_template('writer.html', text=poem, fname=choice[1], type=type)
    users = session['users']
    username = users['username']
    count = mypoem.find({'user': username}).count()
    subscribers = mySub.find({'pid':users['username']}).count()

    if subCount > 0:
        last = mylast.find_one({'uid':users['username']})
        lastseen = last['lasttime']
        #     print(lastseen)
        #     for poet in x:
        #         if mypoem.find({'user':poet['pid'], 'datetime':{'$gte':lastseen}}).count() > 0:
        #             newly_added = mypoem.find({'user':poet['pid'], 'datetime':{'$gte':lastseen}})
        #             mynoti.insert_one({'uid':users['username'], 'poet':poet['pid'], 'corp':newly_added})
        notifs = mynoti.find({'uid':users['username'], 'dateTime':{'$gte':lastseen}})
    return render_template('profile.html', users=users, count=count, type=type, subList=subList, subscribers=subscribers, cnt=subCount, notifs=notifs)


@app.route('/help')
def help():
    users = session['users']
    type = users['type']
    return render_template('help.html', type=type)


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    global users
    users = session['users']
    type = users['type']
    name = session['epname']
    x = " "
    data = {}
    # try:
    #     if session['data'] is not None:
    #         # print("data :"+ session['data'])
    #         data = session['data']
    # except KeyError:
    #     data = {}
    if request.method == "POST":
        name = session['epname']

        if "view" in request.form:
            view = request.form['view']
            rec = mypoem.find_one({'poem_name': view})
            text = rec["poem"]
            x = rec["poem_name"]
            session["text"] = text
            session["fname"] = x
            session['flag'] = 'disabled'
            return render_template('writer.html', text=text, fname=x, type=type, flag='disabled')

        name = request.form['name'].strip()
        if name != users['username']:
            session['epname'] = name
            if mypoem.find({'user': name, 'draft': False}) is not None:
                data = mypoem.find({'user': name, 'draft': False})
            if mypoem.find_one({'poem_name': name, 'draft': False}) is not None:
                data = mypoem.find({'poem_name': name, 'draft': False})

    return render_template('explore.html', name=name, data=data, type=type)


@app.route('/poets', methods=['GET', 'POST'])
def poets():
    users = session['users']
    type = users['type']
    uname = users['username']
    poetList = mytbl.find({'type': 'poet'})
    poet = []
    cnt = []
    no_of_sub = []
    sub_stat = []
    state = 0
    for poem in poetList:
        if poem['username'] != uname:
            poet.append(poem['username'])
    length = len(poet)
    for pname in poet:
        if mySub.find_one({'uid': users['username'], 'pid': pname}):
            sub_stat.append(1)
            print(1)
        else:
            sub_stat.append(0)
            print(0)
        no_of_sub.append(mySub.find({'pid': pname}).count())  # number of subscribers
        c = mypoem.find({'user': pname, 'draft': False}).count()  # number of poems by poet
        cnt.append(c)

    def basic():
        users = session['users']
        type = users['type']
        uname = users['username']
        poetList = mytbl.find({'type': 'poet'})
        poet = []
        cnt = []
        no_of_sub = []
        sub_stat = []
        state = 0
        for poem in poetList:
            if poem['username'] != uname:
                poet.append(poem['username'])
                # print(poem['username'])
        length = len(poet)
        for pname in poet:
            if mySub.find_one({'uid': users['username'], 'pid': pname}):
                sub_stat.append(1)
                # print(1)
            else:
                sub_stat.append(0)
                # print(0)
            no_of_sub.append(mySub.find({'pid': pname}).count())  # number of subscribers
            c = mypoem.find({'user': pname, 'draft': False}).count()  # number of poems by poet
            cnt.append(c)

    if request.method == 'POST':
        stat = request.form['subscribe']
        choice = stat.split(" ")
        pid = choice[0]
        color = choice[1]
        uid = users['username']
        if color == "blue":
            chcksubData = mySub.find_one({'uid': uid, 'pid': pid})
            if chcksubData is None:
                subData = {'uid': uid, 'pid': pid}
                mySub.insert_one(subData)
            else:
                state = chcksubData
        elif color == "red":
            mySub.delete_one({'uid':uid, 'pid':pid})
        basic()
    return render_template('poets.html', type=type, poet=poet, len=length, state=state, count=cnt, sub=no_of_sub, sub_stat=sub_stat)


@app.route('/play_poems', methods=['POST','GET'])
def machine():
    # if request.method == "POST":
    #     line1 = request.form['line1']
    #     line2 = request.form['line2']
        # text1 = mp.predict(line1,20)
        # text2 = mp.predict(line2,20)
        # text = text1 + "\n" + "\n" + text2
        # return render_template('machine_gened_poem.html', text=text)
    return render_template('machine_gened_poem.html')


if __name__ == '__main__':
    app.run(debug=True)

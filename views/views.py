from app import app,db
from flask import render_template,request,redirect,session,url_for,jsonify
from models.models import Polls,Users,Pollvote

@app.route('/',methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username = username,password = password).first()
        if user:
            cur_user = user.username
            session['user_val'] = '%s' % (cur_user,)
            print(cur_user)
            return redirect(url_for('polls'))
        else:
            return jsonify({'msg':'user not found'})
    else:
        return render_template('login.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            newuser = Users(username = username,password = password)
            db.session.add(newuser)
            print('done')
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return jsonify({'msg':'user already exists'})
    else:
        return render_template('register.html')
@app.route('/polls',methods = ['GET','POST'])
def polls():
    user_val = session.get('user_val',None)
    user = Users.query.filter_by(username = user_val).first()
    if request.method == 'POST':
        question = request.form['question']
        choice1 = request.form['choice1']
        choice2 = request.form['choice2']
        newpoll = Polls(question = question,choice1 = choice1,choice2 = choice2,owner = user)
        db.session.add(newpoll)
        db.session.commit()
        return redirect(url_for('polls'))
    else:
        questions = Polls.query.all()
        return render_template('polls.html',polls = questions,user = user)

@app.route('/polls/<int:id>',methods = ['POST'])
def poll(id):
    user_val = session.get('user_val',None)
    user = Users.query.filter_by(username = user_val).first()
    if request.method == 'POST':
        poll = Polls.query.filter_by(id = id).first()
        print(poll)
        selected = request.form.get('choice')
        print(selected)
        if selected == poll.choice1:
            voting = Pollvote(user_id = user.id,poll_id = poll.id)
            poll.choice1_total = 1
            poll.selected = selected
        elif selected == poll.choice2:
            voting = Pollvote(user_id = user.id,poll_id = poll.id)
            poll.choice2_total = 1
            poll.voted = user.id
            poll.selected = selected
        db.session.add(poll)
        db.session.add(voting)
        db.session.commit()
        return redirect(url_for('polls'))
@app.route('/logout')
def logout():
    return redirect(url_for('login'))


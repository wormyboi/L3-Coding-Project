from flask import Flask, render_template, request
import random

app = Flask(__name__)

#Set up
#If the user is signed in, username
user = ["no", "n/a"]

#Temporary dictionary - will be replaced with database
user_ids = {"bleh": "password123"}

#Reccomended modules to be displayed on home page
recs = ["rips", "holes", "waves"]

#selected module
module=["none"]

questions = []

ans = {}

#Dictionaries containing quiz / module questions
rips_mod = {}
rips_quiz = {
    1: {"var1": "ans", "var2": "ans", "var3": "ans"}, 
    2: {"variant1": "ans", "varient2": "ans", "varient3": "ans"}
    }
waves_mod = {}
waves_quiz = {}

user_ans = {}

#App Routes
#home page
@app.route('/')
def home():
    return render_template('index.html', signin=user[0])

#all modules page
@app.route('/modules')
def modules():
    return render_template('modules.html', signin=user[0])

#attempted modules page
@app.route('/attempted')
def attempted():
    return render_template('attempted.html', signin=user[0])

#profile page
@app.route('/profile')
def profile():
    return render_template('profile.html', username=user[1], signin=user[0])

#sign up page
@app.route('/signup')
def signup():
    return render_template('signup.html')
#When user attempts to sign up:
@app.route('/sign', methods=["POST"])
def sign():
    username = request.form.get("sign_user")
    password = request.form.get("sign_pass")
    #Checks if username already exists
    if username in user_ids.keys():
        error_statement = "Username is already taken."
        return render_template('signup.html', error_statement=error_statement)
    else:
        #Adds account details to dictionary, logs user in, and returns to
        #the home page if not
        user_ids[username] = password
        user[0] = "yes"
        user[1] = username
        return render_template("index.html", signin=user[0])

#log in poage
@app.route('/login')
def login():
    return render_template('login.html')
#When user attempts to log in:
@app.route('/log', methods=["POST"])
def log():
    username = request.form.get("log_user")
    password = request.form.get("log_pass")
    #Returns to log in page with error statement if username and password
    #aren't both filled in
    if not username or not password:
        error_statement = "Please fill in all feilds"
        return render_template("login.html", error_statement=error_statement,
                            log_user=username, log_pass=password)
    else:
    #Checks if username and password exist
        if username in user_ids.keys():
            if user_ids[username] == password:
        #Logs the user in and returns them to the home page if so
                user[0] = "yes"
                user[1] = username
                return render_template("index.html", signin=user[0])
        #Returns error statement if not
        error_statement = "Username and password do not match"
        return render_template("login.html", error_statement=error_statement,
                            log_user=username, log_pass=password)


#Logs user out and returns them to the home page   
@app.route('/logout', methods=["POST"])
def logout():
    user[0] = "no"
    user[1] = "n/a"
    return render_template("index.html", signin=user[0])

@app.route('/quiz')
def quiz():
    questions.clear()
    ans = {}
    quesnum = 0
    module[0] = "Quiz - Rips" #   REMOVE LATER!!!!!!!!!!!!!!!!!!!
    #Putting together a set of questions 
    if module[0] == "Quiz - Rips":
        tp = "quiz"
        for num in rips_quiz.keys():
            pos = rips_quiz[num]
            pos_questions = []
            for i in pos.keys():
                pos_questions.append(i)
            q = random.choice(pos_questions)
            questions.append(q)
            ans[q] = pos[q]
            quesnum +=1
    #Current question number
    no = 0
    num = "0"
    return render_template("quizbase.html", module=module[0], questions=questions, ans=ans, quesnum=quesnum, tp=tp, no=no, num=num)

@app.route('/quizpage', methods=["POST"])
def quizpage():
    quesnum = len(questions)
    act_type = request.form.get("act_type")
    num = request.form.get("q_num")
    no = int(num)
    if act_type == "next":
        no +=1
        num=str(no)
    mod = module[0]
    modu = mod.split()
    if modu[0] == "Quiz":
        tp = "quiz"
    else:
        tp = "module"
    return render_template("quizbase.html", no=no, module=module[0], questions=questions, ans=ans, tp=tp, quesnum=quesnum, num=num)

@app.route('/endquiz', methods=["POST"])
def endquiz():
    quesnum = len(questions)
    score = 0
    #for q in ans.keys():
    #    if ans[q] == user_ans[q]:
    #        score +=1
    return render_template("endquiz.html", signin=user[0], quesnum=quesnum, score=score)


#Run program
if __name__ == '__main__':
    app.run(debug=True)
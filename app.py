from flask import Flask, render_template, request
import random

app = Flask(__name__)

#Set up
#If the user is signed in, username
user = ["no", "n/a"]

#Temporary dictionary - will be replaced with database
user_ids = {"bleh": "password123"}

#Reccomended modules to be displayed on home page
recs = ["Quiz - Rips", "Quiz - Holes", "Quiz - Waves"]

#selected module
module=["none"]

questions = []

ans = {}

user_ans = {}
high_scores = {"Quiz - Rips": 0, "Quiz - Holes": 0, "Quiz - Waves": 0}

#Modules / quizzes that are in progress
c_atmpt = []
#Completed modules / quizzes
completem = []
completeq = []

#Image information for each of the module / quiz cards on the modules / home pages
#"quiz / module name": ["src", "alt"]
modcard = {
    "Rips": ["{{ url_for('static', filename='temp_ripcard.jpg') }}", "rip current"], 
    "Waves": ["{{ url_for('static', filename='temp_wavecard.jpg') }}", "wave"], 
    "Holes": ["{{ url_for('static', filename='temp_holecard.jpg') }}", "beach with exposed holes"], 
    "Quiz - Rips": ["{{ url_for('static', filename='temp_ripcard.jpg') }}", "rip current"], 
    "Quiz - Holes": ["{{ url_for('static', filename='temp_holecard.jpg') }}", "beach with exposed holes"], 
    "Quiz - Waves": ["{{ url_for('static', filename='temp_wavecard.jpg') }}", "wave"]
    }

#contain user answers for attempts currently in progress
user_ans_rips = {}
user_ans_holes = {}
user_ans_waves = {}
user_ans_ripsmod = {}
user_ans_holesmod = {}
user_ans_wavesmod = {}
#contains question sets for attempts currently in progress
qset_rips = []
qset_holes = []
qset_waves = []
qset_ripsmod = []
qset_holesmod = []
qset_wavesmod = []
#"Quiz / module name": [user answers, question set, current question number]
ans_dicts = {
    "Quiz - Rips": [user_ans_rips, qset_rips, 0], "Quiz - Waves": [user_ans_waves, qset_waves, 0], 
    "Quiz - Holes": [user_ans_holes, qset_holes, 0], "Rips": [user_ans_ripsmod, qset_ripsmod, 0], 
    "Waves": [user_ans_wavesmod, qset_wavesmod, 0], "Holes": [user_ans_holesmod, qset_holesmod, 0]
    }

 #which questions are no longer able to be answered
q_lock = {}


#Dictionaries containing quiz / module questions and their answers
rips_mod = {
    1: {"Starting info": ["infopage", "n/a"]},
    2: {"Follow up q (prob abt identification)": ["checkbox", "ans", "not ans", "other ans", "3rd ans", "other not ans"]},
    3: {"Further info": ["infopage", "n/a"]},
    4: {"Video maybe": ["infopage", "n/a"]},
    5: {"another q (maybe with img options)": ["checkbox", "correct", "no", "also no"]},
    6: {"identifying q 2 (from shore this time)": ["checkbox", "right", "wrong", "wrong again"]},
    7: {"Escaping rips(?)": ["infopage", "n/a"]},
    8: {"q abt prev info": ["radio", "ans", "not ans"]}
}
rips_quiz = {
    1: {
        "var1": ["text", "ans"], "var2": ["text", "ans"], "var3": ["text", "ans"]
        }, 
    2: {
        "variant1": ["radio", "correct ans", "incorrect ans", "wrong ans"], 
        "varient2": ["radio", "correct ans2", "not-right ans"], 
        "varient3": ["radio", "correct ans3", "incorrect", "wrong", "very wrong"]
        },
    3: {
        "Var 1": ["checkbox", "ans", "not-ans", "v-not-ans"],
        "Var 2": ["checkbox", "right", "wrong", "not this one"]
        },
    }
waves_mod = {}
waves_quiz = {
    1: {
        "question1": ["radio", "answer that is right", "answer that isn't", "other answer that isn't"],
        "question1 the 2nd": ["radio", "This one's right", "something false abt waves", "idk anymore"],
        "question1 the 3rd": ["radio", "correct ans", "aaaaa", "definitely wrong ans"]
    },
    2: {
        "the second wave question": ["text", "ans"], 
        "the second second wave question": ["text", "ans"],
        "the second second second wave question": ["text", "ans"]
    },
    3: {
        "wave q the 3rd": ["radio", "definetly correct ans", "100% wrong ans", "don't click this one if u want to be right"],
        "wave q the 3rd the 2nd": ["radio", "right", "not right"]
    },
    4: {
        "MEEeowwwwww": ["text", "doppler"],
        "wawawawa": ["text", "beats me"]
    },
}
holes_mod = {}
holes_quiz = {
    1: {
        "holes q goes here": ["checkbox", "right", "wrong"],
        "holes q goes here too": ["checkbox", "right", "not right", "I'm so tired"],
        "holes q also goes here": ["checkbox", "correct", "incorrect", "aaaaaa"]
    },
    2: {
        "yipee! last placeholder q": ["text", "ans"],
        "last last placeholder q": ["text", "ans"],
        "last placeholder q the final season": ["text", "ans"],
        "last placeholder q the final season the finale (real, not clickbait)": ["radio", "I belive you!", "theres more isn't there !",
                                                                                  "you lack credibilty", "I don't know what to believe anymore"],
    },
}
#contains innermost lists from above dictionaries for selected questions
var_info = []

#App Routes
#home page
@app.route('/')
def home():
    return render_template('index.html', signin=user[0])

#all modules page
@app.route('/modules')
def modules():
    return render_template('modules.html', signin=user[0], modcard_info=modcard)

#attempted modules page
@app.route('/attempted')
def attempted():
    c_len = len(c_atmpt)
    completem_len = len(completem)
    completeq_len = len(completeq)
    return render_template('attempted.html', signin=user[0], c_atmpt=c_atmpt, completem=completem,
                            completeq=completeq, modcard_info=modcard, c_len=c_len,
                            completem_len=completem_len, completeq_len=completeq_len, hs=high_scores)

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

@app.route('/quiz', methods=["POST"])
def quiz():
    q_ans = ""
    q_lock.clear()
    questions.clear()
    user_ans.clear()
    ans.clear()
    var_info.clear()
    opt = []
    checked = {}
    quesnum = 0
    #Setting up question sets for selected module / quiz
    module[0] = request.form.get("act")
    attempt = ans_dicts[module[0]]
    #continuing an attempt
    if len(attempt[1]) >= 1:
        no = attempt[2]
        for q in attempt[1]:
            questions.append(q)
        prev_ans = attempt[0]
        if type(prev_ans) == dict:
            for q in prev_ans.keys():
                user_ans[q] = prev_ans[q]
            if module[0] == "Quiz - Rips":
                tp = "quiz"
                #Setting up ans dictionary
                for num in rips_quiz.keys():
                    pos = rips_quiz[num]
                    #Adding question info associated with varient from previous attempt
                    #to var_info
                    var_info.append(pos[questions[quesnum]])
                    var_list = var_info[quesnum]
                    ans[questions[quesnum]] = var_list[1]
                    #If the question has already been answered, lock it
                    if questions[quesnum] in user_ans.keys():
                        q_lock[quesnum] = "disabled"
                    quesnum +=1
            elif module[0] == "Quiz - Holes":
                tp = "quiz"
                for num in holes_quiz.keys():
                    pos = holes_quiz[num]
                    var_info.append(pos[questions[quesnum]])
                    var_list = var_info[quesnum]
                    ans[questions[quesnum]] = var_list[1]
                    if questions[quesnum] in user_ans.keys():
                        q_lock[quesnum] = "disabled"
                    quesnum += 1
            elif module[0] == "Quiz - Waves":
                tp = "quiz"
                for num in waves_quiz.keys():
                    pos = waves_quiz[num]
                    var_info.append(pos[questions[quesnum]])
                    var_list = var_info[quesnum]
                    ans[questions[quesnum]] = var_list[1]
                    if questions[quesnum] in user_ans.keys():
                        q_lock[quesnum] = "disabled"
                    quesnum += 1
    #starting a new attempt
    else:
        #Puts together a question set for the relevant quiz / module
        #Setting up quiz questions
        if module[0] == "Quiz - Rips":
            tp = "quiz"
            for num in rips_quiz.keys():
                pos = rips_quiz[num]
                pos_questions = []
                for i in pos.keys():
                    pos_questions.append(i)
                q = random.choice(pos_questions)
                questions.append(q)
                var_info.append(pos[q])
                var_list = var_info[quesnum]
                ans[q] = var_list[1]
                quesnum +=1
        elif module[0] == "Quiz - Holes":
            tp = "quiz"
            for num in holes_quiz.keys():
                pos = holes_quiz[num]
                pos_questions = []
                for i in pos.keys():
                    pos_questions.append(i)
                q = random.choice(pos_questions)
                questions.append(q)
                var_info.append(pos[q])
                var_list = var_info[quesnum]
                ans[q] = var_list[1]
                quesnum +=1
        elif module[0] == "Quiz - Waves":
            tp = "quiz"
            for num in waves_quiz.keys():
                pos = waves_quiz[num]
                pos_questions = []
                for i in pos.keys():
                    pos_questions.append(i)
                q = random.choice(pos_questions)
                questions.append(q)
                var_info.append(pos[q])
                var_list = var_info[quesnum]
                ans[q] = var_list[1]
                quesnum +=1
        #Setting up module questions
        elif module[0] == "Rips":
            tp = "module"
            for num in rips_mod.keys():
                pos = rips_mod[num]
                pos_questions = []
                for i in pos.keys():
                    pos_questions.append(i)
                q = random.choice(pos_questions)
                questions.append(q)
                var_info.append(pos[q])
                var_list = var_info[quesnum]
                ans[q] = var_list[1]
                quesnum +=1
        no = 0
    num = str(no)
    var_list = var_info[no]
    #If the question has a radio or checkbox input, sets up a list of options.
    if (var_list[0] != "text") and (var_list[0] != "infopage"):
        for optn in var_list:
            if optn != var_list[0]:
                opt.append(optn)
                if questions[no] in user_ans.keys():
                    if user_ans[questions[no]] == optn:
                        checked[optn] = "checked"
                    else:
                        checked[optn] = ""
                else:
                    checked[optn] = ""
        random.shuffle(opt)
    #If the question has a text input, checks if it's already been answered
    #and sets the answer as a placeholder if so.
    else:
        if questions[no] in user_ans.keys():
            q_ans = user_ans[questions[no]]
    if no not in q_lock.keys():
        q_lock[no] = ""
    #Renders 1st / current question (depending on whether an attempt's in progress)
    return render_template("quizbase.html", module=module[0], questions=questions,
                            ans=ans, quesnum=quesnum, tp=tp, no=no, num=num, 
                            var_list=var_list, opt=opt, signin=user[0], checked=checked,
                            q_lock=q_lock[no], q_ans=q_ans)

@app.route('/quizpage', methods=["POST"])
def quizpage():
    opt = []
    checked = {}
    #setting up local variables again
    quesnum = len(questions)
    act_type = request.form.get("act_type")
    num = request.form.get("q_num")
    u_ans = request.form.get("u_ans")
    no = int(num)
    if no not in q_lock.keys():
        q_lock[no] = ""
    if (no+1) not in q_lock.keys():
        q_lock[no+1] = ""
    #initially setting up as though there are no messages
    msg = False
    msgtype = "none"
    #if this is a module or a quiz
    mod = module[0]
    modu = mod.split()
    if modu[0] == "Quiz":
        tp = "quiz"
    else:
        tp = "module"
    #Checking user answer or moving to the next page
    if act_type == "next":
        no +=1
        num=str(no)
    elif act_type == "submit":
        if u_ans:
            q = questions[no]
            user_ans[q] = u_ans
            if tp == "quiz":
                q_lock[no] = "disabled"
        else:
            msgtype = "errormsg"
            msg = "Please enter an answer"
    if questions[no] in user_ans.keys():
        q = questions[no]
        q_ans = user_ans[q]
        if user_ans[q] == ans[q]:
            msg = "Correct answer! Good job!"
            msgtype = "msg"
        else:
            msg = "Incorrect"
            msgtype = "errormsg"
    else:
        q_ans = ""
    #Setting var_list to the list of information for the question that's
    #going to be displayed and setting up a list of options if necessary
    var_list = var_info[no]
    if (var_list[0] != "text") and (var_list[0] != "infopage"):
        for optn in var_list:
            if optn != var_list[0]:
                opt.append(optn)
                if q_ans == optn:
                    checked[optn] = "checked"
                else:
                    checked[optn] = ""
        random.shuffle(opt)
    #Goes back to quizbase webpage with a message checking the user is ready 
    #to submit their attempt if they click 'finish quiz'
    if act_type == "check":
        if len(user_ans) < len(ans):
            error_message = "Are you sure you want to finish this attempt?\nSome questions are unanswered"
            return render_template("quizbase.html", signin=user[0], quesnum=quesnum, error_message=error_message, no=no,
                                module=module[0], questions=questions, ans=ans, tp=tp, num=num, var_list=var_list, opt=opt,
                                q_lock=q_lock[no], q_ans=q_ans, checked=checked)
        else:
            error_message = "Are you sure you want to finish this attempt?"
            return render_template("quizbase.html", signin=user[0], quesnum=quesnum, error_message=error_message, no=no,
                                module=module[0], questions=questions, ans=ans, tp=tp, num=num, var_list=var_list, opt=opt,
                                q_lock=q_lock[no], q_ans=q_ans, checked=checked)
    #Sends user back to quizbase, either with the next question or their answers checked
    else:
        return render_template("quizbase.html", no=no, module=module[0], questions=questions, ans=ans, tp=tp, 
                               quesnum=quesnum, num=num, var_list=var_list, opt=opt, signin=user[0], msg=msg, msgtype=msgtype,
                               q_lock=q_lock[no], q_ans=q_ans, checked=checked)

@app.route('/endquiz', methods=["POST"])
def endquiz():
    attempt = ans_dicts[module[0]]
    dex = 0
    for num in attempt:
        if type(num) == list or type(num) == dict:
            num.clear()
            attempt[dex] = num
            dex += 1
        else:
            attempt[dex] = 0
    ans_dicts[module[0]] = attempt
    quesnum = len(questions)
    score = 0
    for q in questions:
        if q not in user_ans.keys():
            user_ans[q] = ""
    for q in ans.keys():
        if ans[q] == user_ans[q]:
            score +=1
    mod = module[0]
    mod = mod.split()
    percent_score = (score/quesnum)*100
    if mod[0] == "Quiz":
        if percent_score > high_scores[module[0]]:
            high_scores[module[0]] = percent_score
    #Removes module / quiz from complete list if it's been completed previously,
    #then adds it back as the 1st item of the list.
    mod = module[0].split()
    if mod[0] == "Quiz":
        if module[0] in completeq:
            completeq.remove(module[0])
        completeq.insert(0, module[0])
    else:
        if module[0] in completem:
            completem.remove(module[0])
        completem.insert(0, module[0])
    #Removes module / quiz from current attempts dictionary
    if module[0] in c_atmpt:
        c_atmpt.remove(module[0])
    return render_template("endquiz.html", signin=user[0], quesnum=quesnum, score=score)

@app.route('/exit', methods=["POST"])
def exit():
    num = request.form.get("q_num")
    attempt = ans_dicts[module[0]]
    prev_ans = attempt[0]
    for a in user_ans.keys():
        prev_ans[a] = user_ans[a]
    attempt[0] = prev_ans
    qs = attempt[1]
    if type(qs) == list:
        for q in questions:
            qs.append(q)
    attempt[1] = qs
    attempt[2] = int(num)
    ans_dicts[module[0]] = attempt
    if module[0] in c_atmpt:
        c_atmpt.remove(module[0])
    c_atmpt.insert(0, module[0])
    return render_template("modules.html", signin=user[0])


#Run program
if __name__ == '__main__':
    app.run(debug=True)
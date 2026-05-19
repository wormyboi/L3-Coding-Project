from flask import Flask, render_template, request

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

#Dictionaries containing quiz / module questions
rips_mod = {}
rips_quiz = {
    "1": {"variant1": "ans", "varient2": "ans", "varient3": "ans"}, 
    "2": {"variant1": "ans", "varient2": "ans", "varient3": "ans"}
    }
waves_mod = {}
waves_quiz = {}

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
    questions = {}
    module[0] = "rips_quiz" #   REMOVE LATER!!!!!!!!!!!!!!!!!!!
    if module[0] == "rips_quiz":
        for num in rips_quiz.keys():
            pos = rips_quiz[num]
    return render_template("quizbase.html", module=module[0])


#Run program
if __name__ == '__main__':
    app.run(debug=True)
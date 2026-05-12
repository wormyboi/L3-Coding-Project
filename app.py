from flask import Flask, render_template, request

app = Flask(__name__)

#Set up
signin = "no"

#App Routes
#home page
@app.route('/')
def home():
    return render_template('index.html', signin=signin)

#all modules page
@app.route('/modules')
def modules():
    return render_template('modules.html', signin=signin)

#attempted modules page
@app.route('/attempted')
def attempted():
    return render_template('attempted.html', signin=signin)

#profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

#log in poage
@app.route('/login')
def login():
    return render_template('login.html')

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
        signin = "yes"
        return render_template("index.html", signin=signin)



if __name__ == '__main__':
    app.run(debug=True)
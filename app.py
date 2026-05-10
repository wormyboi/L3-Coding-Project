from flask import Flask, render_template

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


if __name__ == '__main__':
    app.run(debug=True)
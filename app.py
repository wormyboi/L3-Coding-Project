from flask import Flask, render_template

app = Flask(__name__)

#home page
@app.route('/')
def home():
    return render_template('index.html')

#modules page
@app.route('/modules')
def modules():
    return render_template('modules.html')

#profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
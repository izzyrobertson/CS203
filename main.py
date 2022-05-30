from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "Invalid credentials. Please try again!"
        else:
            return redirect(url_for('menu'))
    return render_template('login.html', error=error)


@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/menu")
def menu():
    return render_template('menu.html')


@app.route("/addplant")
def addplant():
    return render_template('addplant.html')


if __name__ == '__main__':
    app.run(debug=True)

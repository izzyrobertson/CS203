from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db = SQLAlchemy(app)


# Create db model
class Plants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(120), nullable=False)
    location = db.Column(db.Text)
    frequency = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<name  %r>' % self.id


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != Users.username or request.form['password'] != Users.password:
            error = "Invalid credentials. Please try again!"
        else:
            return redirect(url_for('menu'))
    return render_template('login.html', error=error)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user_firstname = request.form['firstname']
        user_lastname = request.form['lastname']
        user_dob = request.form['dob']
        user_username = request.form['username']
        user_password = request.form['password']
        new_user = Users(firstname=user_firstname, lastname=user_lastname, dob=user_dob, username=user_username,
                         password=user_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/register')
    else:
        users = Users.query.order_by(Users.date_added)
        return render_template('register.html', users=users)


@app.route("/menu")
def menu():
    return render_template('menu.html')


@app.route("/addplant", methods=['POST', 'GET'])
def addplant():
    if request.method == "POST":
        plant_name = request.form['name']
        plant_type = request.form['type']
        plant_location = request.form['location']
        plant_frequency = request.form['frequency']
        new_plant = Plants(name=plant_name, type=plant_type, location=plant_location, frequency=plant_frequency)
        db.session.add(new_plant)
        db.session.commit()

        return redirect('/addplant')

    else:
        plants = Plants.query.order_by(Plants.date_added)
        return render_template('addplant.html', plants=plants)


@app.route("/myplants", methods=['GET'])
def myplants():
    plants = Plants.query.order_by(Plants.date_added)
    return render_template('myplants.html', plants=plants)


@app.route("/delete/<int:id>")
def delete(id):
    plant_to_delete = Plants.query.get_or_404(id)
    db.session.delete(plant_to_delete)
    db.session.commit()
    return redirect('/myplants')


@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
    plant_to_update = Plants.query.get_or_404(id)
    if request.method == 'POST':
        plant_to_update.name = request.form['name']
        plant_to_update.type = request.form['type']
        plant_to_update.location = request.form['location']
        plant_to_update.frequency = request.form['frequency']
        db.session.commit()
        return redirect('/myplants')
    else:
        return render_template('update.html', plant_to_update=plant_to_update)


if __name__ == '__main__':
    app.run(debug=True)

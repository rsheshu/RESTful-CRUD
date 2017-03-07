from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    _users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    fname = db.Column(db.String(64), unique=True)
    lname = db.Column(db.String(64), unique=True)
    ## address = db.relationship('Address', backref='user_address')

    def __init__(self, name, fname, lname):
        self.name = name
        self.fname = fname
        self.lname = lname

    def __repr__(self):
        return '<Users %r>' % self.name


class Address(db.Model):
    __tablename__ = 'address'
    _addr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _user_id = db.Column(db.Integer, db.ForeignKey('users._users_id'))
    address = db.Column(db.String(256), unique=True, index=True)

    def __init__(self, address, userid):
        self.address = address
        self._user_id = userid

    def __repr__(self):
        return '<Address %r>' % self.address

db.create_all()


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/")
@app.route("/users/newuser")
def newuser():
    return render_template("users.html")


def OK():
    return render_template("home")


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == "POST":
        name = (request.form.get("name"))
        fname = (request.form.get("fname"))
        lname = (request.form.get("lname"))
        addresses = (request.form.get("address"))

        if name and fname and lname:
            newuser = Users(name, fname, lname)
            db.session.add(newuser)
            db.session.commit()
        if addresses:
            print(addresses)
            newaddress = Address(addresses, newuser._users_id)
            print(newaddress)
            db.session.add(newaddress)
            db.session.commit()
    return redirect(url_for("home"))


@app.route("/users/listusers")
def listusers():
    persons = Users.query.all()
    addrss = {}
    for person in persons:
        addr = Address.query.filter_by(_user_id=person._users_id).all()
        print(addr)
        addrss[person._users_id] = addr
    print(persons)
    return render_template("listusers.html", persons=persons, address=addrss)

if __name__ == "__main__":
    app.run(debug=True)




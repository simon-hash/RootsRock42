from flask import Flask, request, Response, render_template
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

from db import db_init, db
from models import Img
from models import Users


app = Flask(__name__)
Bootstrap(app)
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:peterlustig@localhost/img'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        if not email:
            return 'No email entered!', 400
        password = request.form['password']
        if not password:
            return 'No password entered!', 400

        user = Users.query.filter_by(email=email).first()
        db.session.add(user)
        db.session.commit()

        if user.email == email and user.password == password:
            return render_template("user.html", user=user.username)
        else:
            return render_template("register.html")
    return render_template('login.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        if not username:
            return 'No username entered!', 400
        email = request.form['email']
        if not email:
            return 'No email entered!', 400
        password = request.form['password']
        if not password:
            return 'No password entered!', 400

        user = Users(username=username,email=email,password=password)
        db.session.add(user)
        db.session.commit()

        return 'User Created!', 200
        return render_template("user.html", user=user)
    return render_template('register.html')


@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.img, mimetype=img.mimetype)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    return render_template('about.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":

        pic = request.files['pic']
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()

        return 'Img Uploaded!', 200
    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
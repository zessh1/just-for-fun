from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template
from flask_migrate import Migrate, migrate






app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Tattoo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    tattoo_size = db.Column(db.String(20), unique=False, nullable=False)
    tatoo_color = db.Column(db.String(20), unique=False, nullable=False)
    price = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"size : {self.tattoo_size}, price: {self.price}"


@app.route('/')
def index():
    tattoos = Tattoo.query.all()
    return render_template('index.html', tattoos=tattoos)
@app.route('/add_data')
def add_data():
    return render_template('add.html')


@app.route('/add', methods=["POST","GET"])
def profile():

    tattoo_size = request.form.get("tattoo_size")
    tattoo_color = request.form.get("tattoo_color")
    price = request.form.get("price")


    if tattoo_size != '' and tattoo_color != '' and price is not None:
        p = Tattoo(tattoo_size=tattoo_size, tatoo_color=tattoo_color, price=price)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/delete/<int:id>')
def erase(id):
	data = Tattoo.query.get(id)
	db.session.delete(data)
	db.session.commit()
	return redirect('/')

@app.route('/update/<int:id>', methods=["POST","GET"])
def update(id):
    data = Tattoo.query.get(id)
    if request.method == "POST":
        data.tattoo_size = request.form['tattoo_size']
        data.tatoo_color = request.form['tattoo_color']
        data.price = request.form['price']
        db.session.commit()
        return redirect('/')
    else:
        return render_template("update.html", data = data)



if __name__ == '__main__':
    app.run(debug=True,)
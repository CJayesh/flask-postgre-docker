from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(65535), nullable=True)

# TODO: move models to separate file
db.create_all()

# TODO: API completion of all lised below
@app.route('/')
def hello_world():
    return '''<h1>User Reviews</h1>'''

@app.route('/review', methods=['GET', 'POST', 'PUT', 'DELETE'])
def review():
    return request.method

@app.route('/product/<product_id>', methods=['GET'])
def product(product_id):
    return "product:{}".format(product_id)

@app.route('/user/<user_id>', methods=['GET'])
def user(user_id):
    return "User: {}".format(user_id)

if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5000,
            debug=True)

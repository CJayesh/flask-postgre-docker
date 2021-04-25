from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)

# TODO: Create separate model file
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(65535), nullable=True)
    review = db.relationship('Review', backref='product', lazy=True)

    def __repr__(self):
        return '<Product: {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class SiteUser(db.Model):
    __tablename__ = "site_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    review = db.relationship('Review', backref='site_user', lazy=True)

    def __repr__(self):
        return '<SiteUser: {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    site_user_id = db.Column(db.Integer, db.ForeignKey('site_user.id'), nullable=False)
    review = db.Column(db.String(65535), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    __table_args__ = (db.UniqueConstraint('product_id', 'site_user_id', name='_product_user_uc'),)

    def __repr__(self):
        return '<Review: {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'site_user_id': self.site_user_id,
            'review': self.review,
            'rating': self.rating
        }

db.create_all()

# TODO: API completion of all lised below
# TODO: Move to separate file
@app.route('/')
def hello_world():
    return '''<h1>User Reviews</h1>'''

@app.route('/review', methods=['GET', 'POST', 'PUT', 'DELETE'])
def review():
    reviews = Review.query.all()
    return jsonify({'reviews': [review.serialize for review in reviews]})

@app.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    products = Product.query.filter_by(id=product_id)
    return jsonify({'product': [product.serialize for product in products]})

@app.route('/user/<user_id>', methods=['GET'])
def user(user_id):
    users = SiteUser.query.filter_by(id=user_id)
    return jsonify({'user': [user.serialize for user in users]})

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)

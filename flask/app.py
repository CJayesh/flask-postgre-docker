from flask import Flask, request, jsonify, render_template
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

# TODO: Move to separate file

def response_message(message, code):
    return jsonify({"message": message}), code

class APIDefinition:
	def __init__(self, method, endpoint, url_param, form_fields):
		self.method = method
		self.endpoint = endpoint
		self.url_param = url_param
		self.form_fields = form_fields

@app.route('/')
def index():
    endpoints = list()
    endpoints.append(APIDefinition("GET", "review", "product_id", []))
    endpoints.append(APIDefinition("POST", "review", "product_id", ["userId", "review", "rating"]))
    endpoints.append(APIDefinition("PUT", "review", "product_id", ["userId", "review", "rating"]))
    endpoints.append(APIDefinition("DELETE", "review", "product_id", ["userId"]))
    endpoints.append(APIDefinition("GET", "product", "product_id", []))
    endpoints.append(APIDefinition("GET", "user", "user_id", []))
    return render_template("index.html", endpoints=endpoints)

@app.route('/review/<int:product_id>')
def get_review(product_id):
    reviews = Review.query.filter_by(product_id=product_id)
    return jsonify({'reviews': [review.serialize for review in reviews]})

@app.route('/review/<int:product_id>', methods=['POST'])
def post_review(product_id):
    user_id = request.form.get('userId', None)
    review = request.form.get('review', None)
    rating = request.form.get('rating', None)
    try:
        review_object = Review(product_id = product_id,
                        site_user_id = user_id,
                        review = review,
                        rating = rating)
        db.session.add(review_object)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return response_message("Failed to insert given data.", 400)

    return response_message("Success", 200)

@app.route('/review/<int:product_id>', methods=['PUT'])
def put_review(product_id):
    user_id = request.form.get('userId', None)
    review = request.form.get('review', None)
    rating = request.form.get('rating', None)

    try:
        review_object = Review.query.filter_by(product_id=product_id,
                                                site_user_id=user_id).first()
        if review_object is None:
            review_object = Review(product_id = product_id,
                        site_user_id = user_id,
                        review = review,
                        rating = rating)
            db.session.add(review_object)
        else:
            review_object.review = review
            review_object.rating = rating
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return response_message("Request failed.", 400)

    return response_message("Success", 200)

@app.route('/review/<int:product_id>', methods=['DELETE'])
def delete_review(product_id):
    user_id = request.form.get('userId', None)
    try:
        Review.query.filter_by(product_id=product_id, site_user_id=user_id).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return response_message("Request failed.", 400)
    return response_message("Success", 200)

@app.route('/product/<int:product_id>')
def product(product_id):
    products = Product.query.filter_by(id=product_id)
    return jsonify({'product': [product.serialize for product in products]})

@app.route('/user/<int:user_id>')
def user(user_id):
    users = SiteUser.query.filter_by(id=user_id)
    return jsonify({'user': [user.serialize for user in users]})

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)

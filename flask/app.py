from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return '''<h1>User Reviews</h1>'''

if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5000,
            debug=True)

from flask import Flask
from Models.models import db
from Controllers.user_controller import user_blueprint
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Maximiliano:Maximus23@localhost/user_management_db'
app.config['UPLOAD_FOLDER'] = 'Static/Images'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(user_blueprint)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)


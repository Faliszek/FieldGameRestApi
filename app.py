from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "FieldGame_8tkHecj>5F.RnbGxG_J$"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# app.config['JWT_CSRF_IN_COOKIES'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# app.config['JWT_ACCESS_CSRF_COOKIE_NAME'] = "csrf_access"
# app.config['JWT_REFRESH_CSRF_COOKIE_NAME'] = "csrf_refresh"

db = SQLAlchemy(app)
jwt = JWTManager(app)

import views, models, resources


api.add_resource(resources.UserRegistration, '/register')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.GameListResource, '/games')
api.add_resource(resources.RiddleListResource, '/game/<int:game_id>')
api.add_resource(resources.UserGamesStatusResource, '/mygames')
api.add_resource(resources.GameProgressResource, '/mygames/<int:game_id>')
api.add_resource(resources.GameStartResource, '/mygames/<int:game_id>/start')
api.add_resource(resources.GameAdvancementResource, '/mygames/<int:game_id>/advance')


@app.before_first_request
def init():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


if __name__ == '__main__':
    app.run()
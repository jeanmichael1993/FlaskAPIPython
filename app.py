from flask import Flask, jsonify
from flask_restful import Api

from blacklist import BLACKLIST
from resources.hotel import Hot, Hotel
from resources.usuario import Usuario, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from resources.site import Site, Sites


app = Flask(__name__)
# conexão de bancos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# criação da secret key
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
api = Api(app)
jwt = JWTManager(app)

# cria banco de dados no primeiro request
@app.before_first_request
def criar_banco():
    banco.create_all()

# verifica se o token está na blacklist
@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

# informa do acesso invalido caso o usuario não esteja logado
@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401


# adicionando uma classe e seu url
api.add_resource(Hot, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Usuario, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(Sites, '/sites')

if __name__ == '__main__':
    from sql_alchemy import banco

    banco.init_app((app))
    app.run(debug=True)

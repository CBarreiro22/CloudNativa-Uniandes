import hashlib
import uuid

from flask import request
from flask_restful import Resource
from modelos import db, Usuario, Tarea, TareaSchema

tarea_schema = TareaSchema()


class CreateUser(Resource):
    def post(self):

        username = request.json["username"]
        password = request.json["password"]
        email = request.json["email"]
        dni = request.json.get("dni", None)


        # if len(password1) < 8:
        #     return {"mensaje": "la cuenta no pudo ser creada, longitud de password debe ser mayor a 8 caracteres."}, 404

        usuario = Usuario.query.filter(Usuario.username == username).first()
        if usuario is not None:
            return {"mensaje": "la cuenta no pudo ser creada, username ya existe."}, 404
        usuario = Usuario.query.filter(Usuario.email == email).first()
        if usuario is not None:
            return {"mensaje": "la cuenta no pudo ser creada, email ya existe."}, 404
        password_encriptado = hashlib.sha256(request.json["password"]).hexdigest()
        #password_encriptado = hashlib.md5(request.json["password1"].encode('utf-8')).hexdigest()
        nuevo_usuario = Usuario(
            username=username, password=password_encriptado, email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"mensaje": "cuenta creada con éxito"}, 200


# class VistaLogin(Resource):
#     def post(self):
#         username = request.json.get("username", None)
#         email = request.json.get("email", None)
#         password_encriptado = hashlib.md5(
#             request.json["password"].encode('utf-8')).hexdigest()
#
#         if email is not None:
#             usuario = Usuario.query.filter(
#                 Usuario.email == email, Usuario.password == password_encriptado).first()
#             db.session.commit()
#             if usuario is None:
#                 return {"mensaje": "cuenta no existe"}, 404
#         elif username is not None:
#             usuario = Usuario.query.filter(
#                 Usuario.username == username, Usuario.password == password_encriptado).first()
#             db.session.commit()
#             if usuario is None:
#                 return {"mensaje": "cuenta no existe"}, 404
#         else:
#             # Handle the case where email is None
#             return {"mensaje": "correo electrónico no proporcionado"}, 400
#
#         # token_acceso = create_access_token(identity=usuario.username)
#         token_acceso = str(uuid.uuid4())
#         return {"token": token_acceso}, 200
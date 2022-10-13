from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Usuario:
	db_name="muro_privado"
	def __init__( self , data ):
		self.id = data['id']
		self.nombre = data['nombre']
		self.apellido = data['apellido']
		self.email = data['email']
		self.password = data['password']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']


	@classmethod
	def save(cls,data):
		query = "INSERT INTO usuarios (nombre,apellido,email, password,created_at,updated_at) VALUES (%(nombre)s,%(apellido)s,%(email)s, %(password)s,NOW(),NOW());"
		return connectToMySQL(cls.db_name).query_db(query, data)

	@classmethod
	def get_all(cls):
		query = "SELECT * FROM usuarios;"
		results = connectToMySQL(cls.db_name).query_db(query)
		usuarios = []
		for user in results:
			usuarios.append(cls(user))
		return usuarios

	@classmethod
	def get_one(cls,data):
		query = "SELECT * FROM users WHERE id = %(id)s;"
		results = connectToMySQL(cls.db_name).query_db(query,data)
		if len(results) < 1:
			return False
		return cls(results[0])


	@classmethod
	def get_by_email(cls,data):
		query = "SELECT * FROM usuarios WHERE email = %(email)s;"
		result = connectToMySQL(cls.db_name).query_db(query,data)
		if len(result) < 1:
			return False
		return cls(result[0])


	@classmethod
	def get_by_id(cls,data):
		query = "SELECT * FROM usuarios WHERE id = %(owner_id)s;"
		result = connectToMySQL(cls.db_name).query_db(query,data)
		if len(result) < 1:
			return False
		return cls(result[0])

	@staticmethod
	def is_valid(usuario):
		is_valid = True
		if len(usuario['nombre']) < 2:
			is_valid = False
			flash("Nombre debe tener al menos 2 caracteres.")
		if len(usuario['apellido']) < 2:
			is_valid = False
			flash("Apellido debe tener al menos 2 caracteres.")
		query = "SELECT * FROM usuarios WHERE email = %(email)s;"
		results = connectToMySQL(Usuario.db_name).query_db(query,usuario)
		if len(results) >= 1:
			flash("Email already taken.")
			is_valid=False
		if not EMAIL_REGEX.match(usuario['email']):
			flash("Email Invalido!!!")
			is_valid=False
		if len(usuario['password']) < 8:
			is_valid = False
			flash("Password debe tener al menos 8 caracteres.")

		has_mayuscula = False
		has_numero = False
		for char in usuario["password"]:
			if char >= 'A' and char <= 'Z':
				has_mayuscula = True
			if char >= '0' and char <= '9':
				has_numero = True
		if has_mayuscula == False:
			is_valid = False
			flash("Password necesita mayúscula.")
		if has_numero == False:
			is_valid = False
			flash("Password necesita número.")

		return is_valid

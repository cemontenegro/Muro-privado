from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math

class Mensaje:
	db_name = 'muro_privado'
	def __init__(self,data):
		self.id = data['id']
		self.contenido = data['contenido']
		self.remitente_id = data['remitente_id']
		self.remitente = data['remitente']
		self.receptor_id = data['receptor_id']
		self.receptor = data['receptor']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']

	def time_span(self):
		now = datetime.utcnow()
		print(now, "HORA FECHA ACTUAL", self.created_at)
		delta =  now - self.created_at
		print(delta.days)
		print(delta.total_seconds())
		if delta.days > 0:
			return f"{delta.days} days ago"
		elif (math.floor(delta.total_seconds() / 60)) >= 60:
			return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
		elif delta.total_seconds() >= 60:
			return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
		else:
			return f"{math.floor(delta.total_seconds())} seconds ago"

	@classmethod
	def get_user_messages(cls,data):
		query = "SELECT usuarios.nombre as remitente, usuarios2.nombre as receptor, mensajes.* FROM usuarios LEFT JOIN mensajes ON usuarios.id = mensajes.remitente_id LEFT JOIN usuarios as usuarios2 ON usuarios2.id = mensajes.receptor_id WHERE usuarios2.id =  %(owner_id)s"
		results = connectToMySQL(cls.db_name).query_db(query,data)
		mensajes = []
		for mensaje in results:
			mensajes.append( cls(mensaje) )
		return mensajes

	@classmethod
	def save(cls,data):
		query = "INSERT INTO mensajes (contenido,remitente_id,receptor_id) VALUES (%(contenido)s,%(remitente_id)s,%(receptor_id)s);"
		return connectToMySQL(cls.db_name).query_db(query,data)

	@classmethod
	def destroy(cls,data):
		query = "DELETE FROM mensajes WHERE mensajes.id = %(id)s;"
		return connectToMySQL(cls.db_name).query_db(query,data)
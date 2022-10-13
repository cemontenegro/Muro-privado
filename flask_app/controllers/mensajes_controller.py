from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.usuario_model import Usuario
from flask_app.models.mensaje_model import Mensaje

@app.route('/post_message',methods=['POST'])
def post_message():
	if 'usuario_id' not in session:
		return redirect('/')

	data = {
		"remitente_id":  request.form['remitente_id'],
		"receptor_id" : request.form['receptor_id'],
		"contenido": request.form['contenido']
	}
	Mensaje.save(data)
	return redirect('/dashboard')

@app.route('/destroy/message/<int:id>')
def destroy_message(id):
	data = {
		"id": id
	}
	Mensaje.destroy(data)
	return redirect('/dashboard')
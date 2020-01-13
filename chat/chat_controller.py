from flask import request
from helpers import jwt_required_socket
from flask_jwt_extended import get_jwt_identity

class ChatController:
	def __init__(self, io, clients):
		self.io = io
		self.clients = clients

	def __getitem__(self, key):
		pass
	
	@jwt_required_socket
	def register(self, *args, **kwargs):
		authenticated = kwargs.get("authenticated", False)
		if not authenticated:
			return False
		sid = request.sid
		user = get_jwt_identity()
		print("Registering new client")
		self.clients.append({"sid" : sid, "username" : user["username"]})
		return True
		

	def relay_message(self, payload):
		from_id = request.sid
		to_user = payload.get("to", None)
		message = payload.get("message", "no data")

		print(payload)
		print("Sending from ", from_id, "to", to_user, "message:", message)

		for user in self.clients:
			if user["username"] == to_user:
				self.io.emit('message', {'message': message}, room=user["sid"])


	def disconnect(self, sid):
		for i, client in enumerate(self.clients):
			print("DISCONNECT!!!")
			print(i, client)
			if client["sid"] == sid:
				del	(self.clients[i])
				print("\nDeleting {} from active list\n".format(client["username"]))

	def _get_user_with_sid(self):
		pass

	def _get_user_with_username(self):
		pass
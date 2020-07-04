from chat import ChatController

def setup_socket_routes(socketio):

    client_store = {}
    chat = ChatController(socketio, client_store)

    @socketio.on('connect')
    def socket_register():
        return chat.register(request.sid)

    @socketio.on('disconnect')
    def socket_disconnect():
        chat.disconnect(request.sid)

    @socketio.on('message')
    def socket_relay_message(data):
        chat.relay_message(data)

    @socketio.on_error()
    def error_handler(e):
        print(str(e))

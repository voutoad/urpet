from server.app import app
from server.routes.main import *
from server.routes.auth import *
from server.routes.user import *

app.add_url_rule('/', view_func=root, methods=['GET'])
app.add_url_rule('/map', view_func=map, methods=['GET', 'POST'])
app.add_url_rule('/about', view_func=about, methods=['GET'])

app.add_url_rule('/auth/login', view_func=login, methods=['POST'])
app.add_url_rule('/auth/register/', view_func=register, methods=['POST'])
app.add_url_rule('/me', view_func=me, methods=['GET'])

from server.app import app
from server.routes.main import *
from server.routes.auth import *
from server.routes.user import *
from server.routes.volunteer_form import *

# WITHOUT REGISTRATION
app.add_url_rule('/', view_func=root, methods=['GET'])
app.add_url_rule('/map', view_func=map, methods=['GET', 'POST'])
app.add_url_rule('/about', view_func=about, methods=['GET'])

# AUTH
app.add_url_rule('/auth/login', view_func=login, methods=['POST'])
app.add_url_rule('/auth/register/', view_func=register, methods=['POST'])
app.add_url_rule('/auth/logout', view_func=logout, methods=['GET'])

# USER INTERFACE
app.add_url_rule('/me', view_func=me, methods=['GET'])
app.add_url_rule('/addopt', view_func=addopt, methods=['GET'])
app.add_url_rule('/overexposure', view_func=overexposure, methods=['GET'])
app.add_url_rule('/urpet', view_func=urpet, methods=['GET'])
app.add_url_rule('/poterashki', view_func=poterashki, methods=['GET'])
app.add_url_rule('/naydenushi', view_func=naydenushi, methods=['GET'])
app.add_url_rule('/add-to-cart/<int:us_id>/<int:an_id>/', view_func=add_animal, methods=['GET'])
app.add_url_rule('/delete-from-cart/<int:us_id>/<int:an_id>/', view_func=delete_animal, methods=['GET'])
app.add_url_rule('/update-profile/', view_func=update, methods=['POST'])

# VOLUNTEER INTERFACE
app.add_url_rule('/vol/', view_func=vol_main)
app.add_url_rule('/vol/found', view_func=found, methods=['GET'])
app.add_url_rule('/vol/pot', view_func=pot, methods=['GET'])
app.add_url_rule('/change-ankete/', view_func=ank_change, methods=['POST'])

# ADMIN INTERFACE

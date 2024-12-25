from app import app
from routes.animal_form import *
from routes.main import *
from routes.auth import *
from routes.user import *
from routes.volunteer_form import *
from routes.catch import *
from routes.admin import *

# WITHOUT REGISTRATION
app.add_url_rule('/', view_func=root, methods=['GET'])
app.add_url_rule('/map', view_func=map_animals, methods=['GET', 'POST'])
app.add_url_rule('/about', view_func=about, methods=['GET'])
app.add_url_rule('/create-form/', view_func=new_animal, methods=['POST'])
app.add_url_rule('/get-lost/', view_func=get_lost, methods=['GET'])
app.add_url_rule('/poter/', view_func=found_animal, methods=['GET'])

# AUTH
app.add_url_rule('/auth/login/', view_func=login, methods=['POST'])
app.add_url_rule('/auth/register/', view_func=register, methods=['POST'])
app.add_url_rule('/auth/logout/', view_func=logout, methods=['GET'])

# USER INTERFACE
app.add_url_rule('/me', view_func=me, methods=['GET'])
app.add_url_rule('/addopt', view_func=addopt, methods=['GET'])
app.add_url_rule('/overexposure', view_func=overexposure, methods=['GET'])
app.add_url_rule('/urpet', view_func=urpet, methods=['GET'])
app.add_url_rule('/poterashki', view_func=poterashki, methods=['GET'])
app.add_url_rule('/naydenushi', view_func=naydenushi, methods=['GET'])
app.add_url_rule(
    '/add-to-cart/<int:us_id>/<int:an_id>/',
    view_func=add_animal,
    methods=['GET'],
)
app.add_url_rule(
    '/delete-from-cart/<int:us_id>/<int:an_id>/',
    view_func=delete_animal,
    methods=['GET'],
)
app.add_url_rule('/update-profile/', view_func=update, methods=['POST'])
# VOLUNTEER INTERFACE
app.add_url_rule('/vol/', view_func=vol_main)
app.add_url_rule('/vol/found', view_func=found, methods=['GET'])
app.add_url_rule('/vol/pot', view_func=pot, methods=['GET'])
app.add_url_rule('/change-ankete/', view_func=ank_change, methods=['POST'])

# ADMIN INTERFACE
app.add_url_rule('/admin/add', view_func=add, methods=['GET'])
app.add_url_rule(
    '/admin/change-form/<int:form_id>/', view_func=change, methods=['GET']
)
app.add_url_rule(
    '/admin/delete-form/<int:form_id>/', view_func=delete, methods=['GET']
)
app.add_url_rule('/admin/lostanimals', view_func=lost_animals, methods=['GET'])
app.add_url_rule(
    '/admin/foundanimals', view_func=found_animals, methods=['GET']
)
app.add_url_rule('/admin/volrequests', view_func=vol_requests, methods=['GET'])
app.add_url_rule('/send-email', view_func=send_email, methods=['GET'])
app.add_url_rule(
    '/delte-vol/<int:vol_id>', view_func=delete_vol, methods=['GET']
)

# CATCH INTERFACE
app.add_url_rule('/catch/lost/', view_func=catch_lost, methods=['GET'])
app.add_url_rule('/catch/found/', view_func=catch_found, methods=['GET'])

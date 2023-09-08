from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from Const import EMPTY, VIS, VISSER, WATER
from functions import to_float, add_message, set_config
from model_sqlalchemy.components.components import Components
from model_sqlalchemy.model import Base, Fishing, Fish, Fisherman, Water

ENV = 'dev'
message = EMPTY
list_object = EMPTY

app = Flask( __name__ )
app = set_config(app, ENV)


def create_app():
    with app.app_context():
        C.init_db()

    return app


db = SQLAlchemy( app, model_class=Base )
C = Components(db)
app = create_app()

# Test
HTML_ADD_FISH = 'fish/add.html'
HTML_ERROR = 'error.html'
HTML_SUCCESS = 'success.html'
"""
E n d p o i n t s
"""


@app.route( '/' )
def index():
    return render_template( 'index.html', rows=[obj.toDict( obj.id ) for obj in db.session.query( Fishing )] )


@app.route( '/<int:id>' )
def fishing(id):
    global list_object

    obj = C.get_first( Fishing, id )
    list_object = obj.name
    if obj.name == VIS:  # Vis
        return render_template(
            'fish/fish.html', fishes=[obj.toDict( obj.id ) for obj in db.session.query( Fish )] )
    elif obj.name == VISSER:  # Visser
        return render_template(
            'fisherman/fishermen.html', fishermen=[obj.toDict( obj.id ) for obj in db.session.query( Fisherman )] )
    elif obj.name == WATER:  # Water
        return render_template(
            'water/water.html', waters=[obj.toDict( obj.id ) for obj in db.session.query( Water )] )
    return redirect( redirect_url() )


@app.route( '/fish/<int:id>' )
def fish(id):
    return render_template( 'fish/details.html', fish=C.get_first( Fish, id ) )


@app.route( '/fisherman/<int:id>' )
def fisherman(id):
    return render_template( 'fisherman/details.html', fisherman=C.get_first( Fisherman, id ) )


@app.route( '/water/<int:id>' )
def water(id):
    return render_template( 'water/details.html', water=C.get_first( Water, id ) )


@app.route( '/submit', methods=['POST'] )
def submit_object():
    if request.method == 'POST':
        if request.form['button'] == 'Reset database':
            C.reset_database()
        return redirect( redirect_url() )


@app.route( '/fish', methods=['POST'] )
# Vissoorten
def species_list():
    if request.method == 'POST':
        if request.form['button'] == 'Back':
            return redirect( redirect_url() )

        if request.form['button'] == 'Toevoegen':
            return render_template( HTML_ADD_FISH, fish=Fish() )


"""
C o m m a n d s
"""


@app.route( '/back', methods=['POST'] )
def back():
    if request.method == 'POST':
        return redirect( redirect_url() )


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'GET':
        if list_object == VIS:
            return render_template( HTML_ADD_FISH, fish=Fish() )
        elif list_object == VISSER:
            return render_template( 'fisherman/add.html', fisherman=Fisherman() )
        elif list_object == WATER:
            return render_template( 'water/add.html', water=Water() )
    render_template(
        HTML_ERROR, message=f'"/create/" unknown method "{request.method}" or unknown action "{list_object}".' )


@app.route( '/add_fish', methods=['POST'] )
def add_fish():
    if request.method == 'POST':
        if request.form['button'] == 'Back':
            return redirect( redirect_url() )
        elif request.form['button'] == 'Toevoegen':
            error_message = EMPTY
            length = to_float( request.form['length'] )
            if length == 0.0:
                error_message = add_message( 'Een geldige waarde voor lengte is verplicht.', error_message )
            pounds = to_float( request.form['pounds'] )
            if pounds == 0.0:
                error_message = add_message( 'Een waarde voor gewicht is verplicht.', error_message )
            # Create object
            fish = Fish( request.form['species'],
                         request.form['variety'],
                         to_float( request.form['length'] ),
                         to_float( request.form['pounds'] ),
                         request.form['note'] )
            if error_message:
                # Redisplay already specified data (and message)
                return render_template( HTML_ADD_FISH, message=error_message, fish=fish )

            C.updert_fish( fish )
            return render_template( HTML_SUCCESS, message=f'Vissoort {fish.species} is toegevoegd of bijgewerkt.' )
    render_template( HTML_ERROR, message=f'"/add_fish" unknown method {request.method} or unknown action.' )


@app.route( '/add_fisherman', methods=['POST'] )
def add_fisherman():
    if request.method == 'POST':
        if request.form['button'] == 'Back':
            return redirect( redirect_url() )
        # Create object
        fisherman = Fisherman( request.form['firstname'], request.form['lastname'],  request.form['note'] )
        C.updert_fisherman( fisherman )
        return render_template(
            HTML_SUCCESS, message=f'Visser {fisherman.firstname} {fisherman.lastname} '
                                    f'is toegevoegd of bijgewerkt.' )
    render_template( HTML_ERROR, message=f'"/add_fisherman" unknown method {request.method} or unknown action.' )


@app.route( '/add_water', methods=['POST'] )
def add_water():
    if request.method == 'POST':
        if request.form['button'] == 'Back':
            return redirect( redirect_url() )
        # Create object
        water = Water( request.form['name'], request.form['type'], request.form['note'] )
        C.updert_water( water )
        return render_template(
            HTML_SUCCESS, message=f'Water {water.name} is toegevoegd of bijgewerkt.' )
    render_template( HTML_ERROR, message=f'"/add_water" unknown method {request.method} or unknown action.' )


"""
G e n e r a l   f u n c t i o n s
"""


def redirect_url(default='/'):
    if default == '/':
        return request.host_url
    return request.args.get( 'next' ) or request.referrer or url_for( default )


if __name__ == '__main__':
    app.run( host='localhost', port=5001 )

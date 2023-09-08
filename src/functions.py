from Const import EMPTY


def set_config(app, env):
    if env == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/CarpPond'
    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = ''

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


def add_message(message, to_message) -> str:
    return f'{to_message}\n{message}' if to_message else message


def to_float(value) -> float:
    if not value or not value.replace( ',', EMPTY ).isdecimal():
        return 0.0
    # Only floating comma is allowed
    lst = list( value )
    if '.' in lst and ',' in lst and -1 < lst.index( ',' ) < lst.index( '.' ):
        return 0.0
    return float( value.replace( '.', EMPTY ).replace( ',', '.' ) )

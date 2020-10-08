import flask


class dbhelper:

    def __init__(self):
        self.db = getattr(flask.g, '_database', None)
        if self.db is None:
            self.db = flask.g._database = sqlite3.connect(DATABASE)

    def init_db(self):
        with app.app_context():
            db = get_db()
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    @flask.app.teardown_appcontext
    def close_connection(self):
        db = getattr(flask.g, '_database', None)
        if db is not None:
            db.close()
import click
import sqlite3
from flask import current_app, g


def dict_factory(cursor, row):
    '''Casts the SQLite Row object into a dictionary.'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DialogDB:

    def _make_dialog_query(self, customer_id, dialog_language):
        '''Constucts the dialog query depending on which parameter
        is present.
        
        Parameters
        ----------
        customer_id (int): The customer ID
        dialog_language (str): The dialog language

        Returns
        -------
        tuple(string, tuple): The query and the values
        '''
        queries = [
            'SELECT * FROM dialogs WHERE customer_id=? AND dialog_language=? ORDER BY dialog_timestamp DESC',
            'SELECT * FROM dialogs WHERE dialog_language=? ORDER BY dialog_timestamp DESC',
            'SELECT * FROM dialogs WHERE customer_id=? ORDER BY dialog_timestamp DESC',
            'SELECT * FROM dialogs ORDER BY dialog_timestamp DESC',
        ]
        if customer_id is not None and dialog_language is not None:
            return queries[0], (customer_id, dialog_language)
        if dialog_language is not None:
            return queries[1], (dialog_language,)
        if customer_id is not None:
            return queries[2], (customer_id,)
        return queries[3], ()

    def __init__(self):
        # Connect to SQLite database instance
        self._db = sqlite3.connect(
            current_app.config['SQLITE_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        self._db.row_factory = dict_factory
        
    def init_db(self, fname):
        '''Initializes the database using the provided schema file.
        
        Parameters
        ---------
        fname (str): Filename of the schema file
        '''
        with current_app.open_resource(fname) as f:
            script = f.read()
            script = script.decode('utf8')
            self._db.executescript(script)
    
    def get_dialog_data(self, customer_id, dialog_language):
        '''Queries dialog data from the database.
        Filters the data using the customer ID and dialog language
        parameters, if provided.
        
        Parameters
        ----------
        customer_id (int): The customer ID
        dialog_language (str): The dialog language

        Returns
        -------
        (list[dict]): The dialog data as a list of dictionaries
        '''
        query, values = self._make_dialog_query(customer_id, dialog_language)
        data = self._db.execute(query, values).fetchall()
        return data

    def insert_dialog_data(self, values):
        '''Inserts dialog data into the database.

        Parameters
        ----------
        values (list[tuple]): The dialogs to insert.
        '''
        query = '''
        INSERT INTO dialogs (customer_id, dialog_id, dialog_text, dialog_language, dialog_timestamp)
        VALUES (?,?,?,?,?)
        '''
        self._db.executemany(query, values)
        self._db.commit()

    def close_db(self):
        '''Closes the database.'''
        self._db.close()


def get_db():
    '''Instantiates the database.'''
    if 'db' not in g:
        g.db = DialogDB()
    return g.db


def close_db(e=None):
    '''Closes the database.'''
    db = g.pop('db', None)
    if db is not None:
        db.close_db()


def init_db(fname):
    '''Initializes the database.'''
    db = get_db()
    db.init_db(fname)


@click.command('init-db')
def init_db_command():
    '''Clears the existing data and creates new tables.'''
    init_db('schema.sql')
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

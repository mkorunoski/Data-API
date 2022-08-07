import json
import redis
from flask import current_app, g


class DialogCache:

    def __init__(self):
        # Connect to local Redis instance
        self._r = redis.Redis(
            host='localhost',
            port=6379,
            db=current_app.config['REDIS_DATABASE']
        )
    
    def get_dialog_data(self, dialog_id):
        '''Retrieves dialog data.
        
        Parameters
        ----------
        dialog_id (int): The dialog ID

        Returns
        -------
        list (tuple): Cached dialog data
        '''
        data = self._r.lrange(dialog_id, 0, -1)
        return list(map(json.loads, data))

    def cache_dialog_data(self, dialog_id, values):
        '''Caches dialog data.
        
        Parameters
        ----------
        dialog_id (int): The dialog ID
        values (tuple): The dialog values
        '''
        self._r.lpush(dialog_id, json.dumps(values))
        # Add expiration time of 8 hours so we don't store
        # unconsent data unpurposely.
        self._r.expire(dialog_id, 8*60*60)
    
    def delete_dialog_data(self, dialog_id):
        '''Deletes dialog data.'''
        self._r.delete(dialog_id)


def get_cache():
    '''Instantiates the cache.'''
    if 'cache' not in g:
        g.cache = DialogCache()
    return g.cache


def close_cache(e=None):
    '''Closes the cache.'''
    cache = g.pop('cache', None)


def init_app(app):
    app.teardown_appcontext(close_cache)

from flask import Blueprint, request, make_response
from dialogs.cache import get_cache
from dialogs.db import get_db


bp = Blueprint('consents', __name__, url_prefix='/consents')


@bp.route('/<int:dialog_id>', methods=['POST'])
def post_consent(dialog_id):
    if 'consent' not in request.json:
        return make_response('Please provide the "consent" parameter', 400)
    
    consent = request.json['consent']

    if not isinstance(consent, bool):
        return make_response('"consent" parameter needs to be of type boolean', 400)

    if not consent:
        try:
            cache = get_cache()
            cache.delete_dialog_data(dialog_id)
            return make_response(f'Cached texts for dialogID={dialog_id} removed succesfully.', 200)
        except Exception as e:
            return make_response(e, 500)

    try:
        cache = get_cache()
        values = cache.get_dialog_data(dialog_id)
        if len(values) == 0:
            return make_response('Cache empty', 200)
        db = get_db()
        db.insert_dialog_data(values)
        cache.delete_dialog_data(dialog_id)
        return make_response(f'Cached texts for dialogID={dialog_id} stored succesfully.', 200)
    except Exception as e:
        return make_response(e, 500)

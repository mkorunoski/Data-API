from datetime import datetime
from flask import Blueprint, current_app, request, make_response
from dialogs.cache import get_cache
from dialogs.db import get_db


bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/', methods=['GET'])
def get_dialog_data():
    customer_id = request.args.get('customerId')
    dialog_language = request.args.get('language')

    if customer_id is not None:
        customer_id = int(customer_id)
        if customer_id < 0:
            return make_response('"customerId" needs to be a positive integer', 400)

    if dialog_language is not None and dialog_language not in current_app.config['SUPPORTED_LOCALES']:
        supported_locales = ', '.join(current_app.config['SUPPORTED_LOCALES'])
        return make_response(f'Unsuported language ({dialog_language}). Curently supported languages: {supported_locales}', 400)

    try:
        db = get_db()
        data = db.get_dialog_data(customer_id, dialog_language)
        return make_response(data, 200)
    except Exception as e:
        return make_response(e, 500)


@bp.route('/<int:customer_id>/<int:dialog_id>', methods=['POST'])
def post_dialog_data(customer_id, dialog_id):
    if 'text' not in request.json or 'language' not in request.json:
        return make_response('Please provide the "text" and "language" parameters', 400)
   
    dialog_text = request.json['text']
    dialog_language = request.json['language']

    if not isinstance(dialog_text, str):
        return make_response('"text" parameter needs to be of type string', 400)
    
    if not isinstance(dialog_language, str):
        return make_response('"language" parameter needs to be of type string', 400)
    
    if dialog_language not in current_app.config['SUPPORTED_LOCALES']:
        supported_locales = ', '.join(current_app.config['SUPPORTED_LOCALES'])
        return make_response(f'Unsuported language ({dialog_language}). Curently supported languages: {supported_locales}', 400)
    
    dialog_timestamp = str(datetime.now())

    try:
        cache = get_cache()
        cache.cache_dialog_data(dialog_id, (customer_id, dialog_id, dialog_text, dialog_language, dialog_timestamp))
    except Exception as e:
        return make_response(e, 500)

    return make_response(f'Text for dialogID={dialog_id} cached succesfully.', 200)

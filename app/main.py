from typing import Optional, List
from fastapi import FastAPI, Query
from app.utils import ModelName, fake_items_db, items_dict
from app.schemas import Item

app = FastAPI()


@app.get('/')
async def index():
    return {'message': 'hello world'}


@app.post('/items/')
async def create_item(item: Item):
    return item


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    return {'item_id': item_id, **item.dict()}


@app.post('/items/calcule_price')
async def calculate_price(item: Item):
    item_dict = item.dict()
    item.tax = item.tax or 0
    calculated_price = item.price - item.tax
    return calculated_price


@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get('/items/{item_name}')
async def read_specific_item_by_name(item_name: str, q: Optional[str] = None):
    if q:
        return {'item_name': item_name, 'q': q}

    return {'item_name': item_name}


@app.get('/items/boolean/{item_id}')
async def read_item_boolean_query(item_id: int, q: Optional[str] = None, short: bool = False):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if short:
        item.update({'description': 'This is a short description'})
    else:
        item.update({'description': 'This is an amazing item that has a long description'})

    return item


@app.get('/items/params/{item_id}')
async def read_params_items(item_id: int, needy: str):
    item = {'item_id': item_id, 'needy': needy}
    return item


@app.get('/items/{item_id}')
async def read_specific_item(item_id: int):
    return {'item_id': item_id}



@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}


@app.get('/users/{user_id}')
async def read_user(user_id: int):
    return {'user_id': user_id}


@app.get('/models/')
async def get_models():
    models_names = []
    models = ModelName
    i = 0
    for model in models:
        models_names.append({i: model.value})
        i += 1
    return models_names


@app.get('/models/{model_name}')
async def get_model_by_name(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep Learning FTW!'}

    if model_name.value == 'lenet':
        return {'model_name': model_name, 'message': 'LeCNN all the images'}

    return {'model_name': model_name, 'message': 'Have some residuals'}


@app.get('/models/params/{model_name}')
async def read_model_params(
    model_name: str, needy: str, skip: int = 0, limit: Optional[int] = None
):
    model = {
        'model_name': model_name,
        'needy': needy,
        'skip': skip,
        'limit': limit or 0
        }
    return model


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}


@app.get('/list_items')
async def read_list_items(q: Optional[str] = Query(None, max_length=50)):
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/get_items')
async def get_list_items(q: Optional[str] = Query(None, min_length=3, max_length=50)):
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/get_items_rgx')
async def get_items_regex(
    q: Optional[str] = Query(None, min_length=3, max_length=50, regex=r"^fixedquery$")
):
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/get_items_default_value')
async def get_items_default_value(q: str = Query("fixedquery", min_length=3, max_length=50)):
    result = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/many_items_query')
async def many_items_query(q: Optional[List[str]] = Query(None)):
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/many_items_query_default')
async def many_items_query(q: List[str] = Query(['aaa', 'bbb'])):
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/items_metadata_title')
async def metadata_title_items(
    q: Optional[str] = Query(None, title='Query String', min_length=3)
):
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/items_metadata_description')
async def metadata_description_items(
    q: Optional[str] = Query(
        None,
        title='Query String',
        description='Query string for the items to search in the database',
        min_length=3,
        max_length=50
    )
):
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/items_alias_query_param')
async def alias_query_param_item(q: Optional[str] = Query(None, alias='item-query')):
    results = items_dict
    if q:
        results.update({'q': q})
    return results

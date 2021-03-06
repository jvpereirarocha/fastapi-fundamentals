from typing import Optional, List, Dict
from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from app.utils import ModelName, fake_items_db, items_dict
from app.schemas import (Item, User, DeclaredItem, Address, Product, UserIn,
    UserOut, GetUser, ProgrammingLanguage)
from datetime import datetime, time, timedelta
from uuid import UUID

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
    """
        Getting default values for query params
    """
    result = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/many_items_query')
async def many_items_query(q: Optional[List[str]] = Query(None)):
    """
        Many query params
    """
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/many_items_query_default')
async def many_items_query(q: List[str] = Query(['aaa', 'bbb'])):
    """
        Many default query params
    """
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/items_metadata_title')
async def metadata_title_items(
    q: Optional[str] = Query(None, title='Query String', min_length=3)
):
    """
        Validating query param size
    """
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
    """
        Inserting metadata to query param
    """
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/items_alias_query_param')
async def alias_query_param_item(q: Optional[str] = Query(None, alias='item-query')):
    """
        Defining an alias to query param
    """
    results = items_dict
    if q:
        results.update({'q': q})
    return results


@app.get('/items/path_params/{item_id}')
async def read_path_params_item(
    item_id: int = Path(..., title='The ID of the item to get'),
    q: Optional[str] = Query(None, alias='item-query'),
):
    """
        Inserting path params metadata
    """
    results = {'item_id': item_id}
    if q:
        results.update({'q': q})
    return results


@app.get('/items/number_validator_ge/{item_id}')
async def number_validator_greather_equals_item(
    *,
    item_id: int = Path(..., title='The ID of the item to get', ge=1),
    q: Optional[str]
):
    """
        Inserting number validator
    """
    results = {'item_id': item_id}
    if q:
        results.update({'q': q})
    return results


@app.get('/items/number_validator_gt_le/{item_id}')
async def number_validator_greather_than_less_equals_item(
    *,
    item_id: int = Path(..., title='The ID of the item to get', gt=0, le=100),
    q: Optional[str]
):
    """
        Inserting number validator
    """
    results = {'item_id': item_id}
    if q:
        results.update({'q': q})
    return results


@app.get('/items/number_validator_float_gt_lt/{item_id}')
async def number_validator_float_greather_than_less_than_item(
    *,
    item_id: int = Path(..., title='The ID of the item to get', ge=0, le=100),
    q: Optional[str],
    size: float = Query(..., gt=0, lt=10.5)
):
    """
        Using validator to item_id (greather than equals 0 and less equals 100)
        and size greather than 0 and less than 10.5
    """

    results = {'item_id': item_id}
    if q:
        results.update({'q': q})
    return results


@app.put('/items/update_optional_item/{item_id}')
async def update_item_optional_body(
    *,
    item_id: int = Path(..., title='The ID of the item to get', ge=0, le=100),
    q: Optional[str] = None,
    item: Optional[Item] = None
):
    """
        Using validator to item_id (greather than equals 0 and less equals 100)
    """

    results = {'item_id': item_id}
    if q:
        results.update({'q': q})
    if item:
        results.update({'item': item})
    return results


@app.put('/items/update_multiple_body/{item_id}')
async def update_item_multiple_body(item_id: int, item: Item, user: User):
    """ Using more than one body item (User and Item) """

    results = {'item_id': item_id, 'item': item, 'user': user}
    return results


@app.put('/items/update_body_extra_field/{item_id}')
async def update_item_singular_extra_value(
    item_id: int, item: Item, user: User, importance: int = Body(...)
):
    """ Updating user with extra value """

    results = {'item_id': item_id, 'item': item, 'user': user, 'importance': importance}
    return results


@app.put('/items/update_multiple_body_query/{item_id}')
async def update_multiple_body_query(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    """
        Using more than one body item (User and Item) and
        checking if importance is greather than 0
    """

    results = {'item_id': item_id, 'item': item, 'user': user, 'importance': importance}
    if q:
        results.update({'q': q})
    return results


@app.put('/items/update_item_embed_body/{item_id}')
async def update_item_embed_body(item_id: int, item: Item = Body(..., embed=True)):
    """ Embeding nested body """

    results = {'item_id': item_id, 'item': item}
    return results


@app.put('/items/update_declared_item/{item_id}')
async def update_declared_item(item_id: int, item: DeclaredItem = Body(..., embed=True)):
    """ Embeding nested body with declared item """

    results = {'item': item}
    return results


@app.get('/adresses/', status_code=200)
async def get_all_adresses():
    """ Getting All Adresses """

    return {'adresses': 'All'}


@app.put('/adresses/{address_id}', status_code=200)
async def update_address(address_id: int, address: Address):
    """ Updating Address """

    return {'adresses': address}


@app.post('/adresses/states', status_code=201)
async def create_state(state: Dict[str, str]):
    """ Using dictionary to create state object """

    return {'states': state}


@app.put('/users/schema_extra/{user_id}', status_code=200)
async def update_user(user_id: int, user: User):
    """ Updating user with schema_extra example """

    results = {'user_id': user_id, 'user': user}
    return results


@app.put('/users/product_body/{product_id}', status_code=200)
async def update_product_body(
    *,
    product_id: int,
    product: Product = Body(
        ...,
        examples={
            "normal": {
                "summary": "Valid",
                "description": "Valid Example of Product Example",
                "value": {
                    "code": "BR52123",
                    "price": 5.40,
                    "quantity": 2
                },
            },
            "invalid": {
                "summary": "Invalid",
                "description": "Invalid Example of Product. Don't send like that",
                "value": {
                    "code": 2123,
                    "price": "5.40",
                    "quantity": 2.7
                },
            },
        },
    ),
):
    """ Setting valid and invalid format body examples """

    results = {'product_id': product_id, 'product': product}
    return results


@app.put('/products/using_other_data_types/{product_id}', status_code=200)
async def update_product_data_types(
    product_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    proccess_after: Optional[timedelta] = Body(None),
):
    """ Update product with different data types """

    start_proccess = start_datetime + proccess_after
    duration = end_datetime - start_proccess
    return {
        'product_id': product_id,
        'start_datetime': start_datetime,
        'end_datetime': end_datetime,
        'repeat_at': repeat_at,
        'proccess_after': proccess_after,
        'start_proccess': start_proccess,
        'duration': duration,
    }


@app.get('/products/', status_code=200)
async def get_products(
    ads_id: Optional[str] = Cookie(None),
    user_agent: Optional[str] = Header(None)
):
    """ Getting Cookie and Header """

    return {'ads_id': ads_id, 'User-Agent': user_agent}


@app.get('/products/disable_conversion', status_code=200)
async def get_products_disable_conversion(
    strange_header: Optional[str] = Header(None, convert_underscores=False)
):
    """
        Disable automatically conversion of _ to -
    """
    return {'strange_header': strange_header}


@app.get('/products/duplicate_header', status_code=200)
async def get_products_duplicate_header(
    x_token: Optional[List[str]] = Header(None)
):
    """
        Duplicate Header
    """
    return {'X-Token values': x_token}


# Don't do this in production! The user password will be showed
@app.post('/userin/', response_model=UserIn, status_code=201)
async def create_userin(user: UserIn):
    """
        Using Response Model to show response like schema UserIn
    """
    return user


@app.post('/userout/', response_model=UserOut, status_code=201)
async def create_userin_show_userout(user: UserIn):
    """
        Using Response Model to show response like schema UserOut
    """
    return user


@app.get('/getusers_schema/', response_model=List[GetUser], status_code=200)
async def get_users_schema():
    """
        Using Response Model to show a list of Users response like schema GetUser
    """
    users = [
        {'email': 'teste@mail.com', 'username': 'test', 'full_name': 'test'},
        {'email': 'foo@mail.com', 'username': 'foo', 'full_name': 'foo'},
        {'email': 'bar@mail.com', 'username': 'bar', 'full_name': 'bar'},
    ]
    return users


@app.get('/languages/all', response_model=List[ProgrammingLanguage], status_code=200)
async def get_all_programming_languages():
    """
        Showing All Programming Languages (including default)
    """
    languages = [
        {"name": 'Python', 'category': 'Back-End'}
    ]
    return languages


@app.get('/languages/some', response_model=List[ProgrammingLanguage], response_model_exclude_unset=True)
async def get_some_languages():
    """
        Showing some programming languages (default languages not showed)
    """
    languages = [
        {"name": 'Python', 'category': 'Back-End'},
        {"name": 'CSS', 'category': 'Front-End'},
    ]
    return languages


@app.get(
    '/languages/include',
    response_model=ProgrammingLanguage,
    response_model_exclude_unset=True,
    response_model_include={'name'}
)
async def include_fields_schema():
    """
        Setting required fields to send when make a request
    """

    return {'name': 'Python', 'category': 'Back-End'}


@app.get(
    '/languages/exclude',
    response_model=ProgrammingLanguage,
    response_model_exclude={'name'}
)
async def include_fields_schema():
    """
        Excluding non-required fields when make a request
        PS: Default languages defined at the schema won't hide the field 'name'
    """

    return {'name': 'Javascript', 'category': 'Front-End'}

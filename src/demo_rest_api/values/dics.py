put_user = {
    "name": "Vasanti Devar2",
    "email": "vasanti_devar_test_xz@welch-batz.name",
    "gender": "Female",
    "status": "Active"
}

post_user = {
    "name": "Vasanti Devar",
    "email": "vasanti_devar_test_xz@welch-batz.name",
    "gender": "Female",
    "status": "Active"
}

delete_user = {
    "code": 204,
    "meta": None,
    "data": None
}

headers = {
    'Authorization': '',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

verified_header = {
    'Content-Type': 'application/json; charset=utf-8'
}

unauthorized_response_body = {
    "code": 401,
    "meta": None,
    "data": {
        "message": "Authentication failed"
    }
}

empty_dict = {}

unprocessable_entity_empty_obj = {
    "code": 422,
    "meta": None,
    "data": [
        {
            "field": "email",
            "message": "can't be blank"
        },
        {
            "field": "name",
            "message": "can't be blank"
        },
        {
            "field": "gender",
            "message": "can't be blank"
        },
        {
            "field": "status",
            "message": "can't be blank"
        }
    ]
}
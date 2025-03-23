from fastapi import Response
from json import JSONEncoder


def ErrorResponse(message: str, status_code: int):
    data = {'message': message}
    return Response(content=JSONEncoder(ensure_ascii=False).encode({'response': data}), status_code=status_code)

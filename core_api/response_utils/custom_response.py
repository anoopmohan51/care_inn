from rest_framework.response import Response

class CustomResponse(Response):
    def __init__(
        self, 
        data=None, 
        status=None, 
        headers=None,
        message=None,
        status_code=None,
        content_type=None,
        count=None
    ):
        if message is None:
            message = []
        body = {
            "data":{"result": data},
            "status": status,
            "message": message,
            "status_code": status_code
        }
        if count:
            body.update({"count": count})
        super().__init__(body, status=200, content_type=content_type)
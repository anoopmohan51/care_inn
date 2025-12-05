from rest_framework.response import Response

class CustomResponse(Response):
    def __init__(
        self, 
        data=None, 
        status=None, 
        headers=None,
        message=None,
        status_code=None,
        content_type=None
    ):
        if message is None:
            message = []
        body = {
            "data": [] if data is None else [data],
            "message": message,
            "status_code": status_code
        }
        super().__init__(body, status=200, content_type=content_type)
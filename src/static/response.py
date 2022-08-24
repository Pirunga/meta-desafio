class Response:
    """
    Response structures.
    """
    def success(self, message: str, data='Done'):
        status_code = 200
        response = {'data': data, 'message': message, 'code': status_code, 'success': True}
        print(response)
        return response, status_code


    def created(self, message: str, data=None):
        status_code = 201
        response = {'data': data, 'message': message, 'code': status_code, 'success': True}
        print(response)
        return response, status_code


    def failed(self, message: str, data=None):
        status_code = 400
        response = {'data': data, 'message': message, 'code': status_code, 'success': False}
        print(response)
        return response, status_code


    def conflict(self, message: str, data=None):
        status_code = 409
        response = {'data': data, 'message': message, 'code': status_code, 'success': True}
        print(response)
        return response, status_code


    def custom(self, message: str, status_code: int, success: bool):
        response = {'message': message, 'code': status_code, 'success': success}
        print(response)
        return response, status_code

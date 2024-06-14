from fastapi import HTTPException, status


class DaoExceptions(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(DaoExceptions):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exist"


class IncorretLoginOrPasswordException(DaoExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Uincorrect login or password"


class NotFoundUpdateException(DaoExceptions):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found for update"


class NotFoundException(DaoExceptions):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class NotFoundByDateException(DaoExceptions):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found notes by that period"

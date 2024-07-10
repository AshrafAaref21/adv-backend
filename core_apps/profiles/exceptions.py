from rest_framework.exceptions import APIException

class CantFollowYourself(APIException):
    """class exception for user cant follow himself."""
    status_code = 403
    default_detail = "You cant't follow yourself"
    default_code = "forbidden"
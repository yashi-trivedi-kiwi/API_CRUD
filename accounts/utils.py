from rest_framework.response import Response


def custom_error_response(status, detail, **kwargs):
    """
    function is used for getting same global error response for all api
    :param detail: error message .
    :param status: http status.
    :return: Json response
    """
    if not detail:
        detail = {}
    return Response({"detail": detail}, status=status, **kwargs)

#def custom_response
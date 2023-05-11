from bottle import response

def _RESPOND(status = 400, error_message = "Unknown error"):
    response.status = status
    return {
        "info": error_message
    }

def get_message(self,e):
    error_messages = []
    if hasattr(e, 'detail'):
        # Handle nested error structure
        if isinstance(e.detail, dict):
            for field, errors in e.detail.items():
                if isinstance(errors, list):
                    for error in errors:
                        if hasattr(error, 'string'):
                            error_messages.append(f"{field}: {error.string}")
                        else:
                            error_messages.append(f"{field}: {str(error)}")
                else:
                    error_messages.append(f"{field}: {str(errors)}")
        else:
            error_messages.append(str(e.detail))
    else:
        error_messages.append(str(e))
    return error_messages
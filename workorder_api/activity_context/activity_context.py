import threading

# Thread-local storage for activity context
_thread_locals = threading.local()

def set_activity_user(user):
    """Set the current user for activity logging"""
    _thread_locals.user = user

def get_activity_user():
    """Get the current user for activity logging"""
    return getattr(_thread_locals, 'user', None)

def clear_activity_user():
    """Clear the current user"""
    if hasattr(_thread_locals, 'user'):
        delattr(_thread_locals, 'user')
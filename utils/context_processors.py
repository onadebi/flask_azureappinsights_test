from flask import Flask

def inject_navigation():
    return {
        'menu_items': [
            {'name': 'home', 'url': '/'},
            {'name': 'health check', 'url': '/health'},
            {'name': 'test error', 'url': '/error'},
            {'name': 'dashboard', 'url': '/dashboard/'}
        ]
    }


def load_contexts(app: Flask):
    """
    Load context processors for the Flask application. Load default navigation items
    and other context variables that should be available in templates.
    This is done beforethe application starts handling requests.

    Args:
        app: Flask application instance
    """
    app.context_processor(inject_navigation)
    
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from ladymarry import api

application = DispatcherMiddleware(api.create_app())


if __name__ == "__main__":
    run_simple('0.0.0.0', 8887, application, use_reloader=True, use_debugger=True)

import logging
import os


logger = logging.getLogger(__name__)


class PrefixMiddleWare(object):
    """
    https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes/36033627#36033627

    modify PATH_INFO to handle the prefixed url.
    modify SCRIPT_NAME to generate the prefixed url.
    """
    def __init__(self, app, prefix=""):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            # strip prefix from PATH_INFO and set SCRIPT_NAME to prefix
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix

            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


class ReverseProxied(object):
    """Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Handle REMOTE_USER
        # logger.info(f"ReverseProxyMiddleware: {environ}")

        # flask_env = os.environ.get('FLASK_ENV', 'production')

        # ru = environ.pop('X_Proxy_Remote_User', None)
        ru = environ.pop('HTTP_X_PROXY_REMOTE_USER', None)
        if os.environ.get('FLASK_ENV', 'production') == 'development':
            ru = os.environ.get('DEV_REMOTE_USER', None)
            logger.debug(f"DEV MODE: Forcing REMOTE_USER to {ru}")

        environ['REMOTE_USER'] = ru

        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


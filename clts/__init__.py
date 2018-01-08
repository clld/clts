from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from clts import models

_ = lambda i: i
_('Contributor')
_('Contributors')
_('Contribution')
_('Contributions')
_('Parameter')
_('Parameters')
_('Value')
_('Values')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')
    return config.make_wsgi_app()

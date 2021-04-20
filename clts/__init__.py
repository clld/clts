from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from clts import models
from clts.interfaces import IFeature

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
    config.include('clldmpg')
    config.register_resource('feature', models.Feature, IFeature, with_index=True)
    return config.make_wsgi_app()

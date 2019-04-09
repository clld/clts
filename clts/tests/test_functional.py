from __future__ import print_function, unicode_literals

import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_dt', '/parameters'),
        ('get_dt', '/values'),
        ('get_html', '/parameters/voiceless_alveolar_click_consonant'),
        ('get_dt', '/values?parameter=voiceless_alveolar_click_consonant'),
        ('get_dt', '/values?contribution=upa'),
        ('get_dt', '/contributions'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)


def test_init():
    from clts.scripts import initializedb
    pass

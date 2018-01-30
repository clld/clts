from setuptools import setup, find_packages


setup(
    name='CLTS',
    version='0.0',
    description='Cross-Linguistic Transcription Systems',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Johann-Mattis List',
    author_email='mattis.list@lingpy.org',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "clldmpg~=3.1",
        'markdown',
    ],
    extras_require={
        'dev': ['flake8', 'waitress'],
        'test': [
            'psycopg2',
            'tox',
            'mock',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="clts",
    entry_points="""\
    [paste.app_factory]
    main = clts:main
    """)

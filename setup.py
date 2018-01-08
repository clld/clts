from setuptools import setup, find_packages


requires = [
    'clld',
]

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
    install_requires=requires,
    tests_require=['mock==1.0'],
    test_suite="clts",
    entry_points="""\
    [paste.app_factory]
    main = clts:main
    """)

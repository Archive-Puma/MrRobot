from setuptools import setup

INFO = {
    'package':      'mrrobot',
    'version':      '1.0',
    'desc_short':   '',
    'desc_long':    '',
    'author_name':  'Kike Fontán (@CosasDePuma)',
    'author_email': 'kikefontanlorenzo@gmail.com',
    'license':      '',
    'url':          'https://github.com/cosasdepuma/mrrobot',
    'platform':     'any',
    'python':       '>=3.8.0'
}

REQUIRES        = []
TEST_REQUIRES   = []
SETUP_REQUIRES  = []

PACKAGES = [ INFO['package'] ]


setup(
    name                =INFO['package'],
    version             =INFO['version'],
    description         =INFO['desc_short'],
    long_description    =INFO['desc_long'],
    author              =INFO['author_name'],
    author_email        =INFO['author_email'],
    license             =INFO['license'],
    url                 =INFO['url'],
    platform            =INFO['platform'],
    python_requires     =INFO['python'],
    install_requires    =REQUIRES,
    setup_requires      =SETUP_REQUIRES,
    tests_require       =TEST_REQUIRES,
    packages            =PACKAGES,
    zip_safe            =False
)

# https://github.com/constverum/ProxyBroker/blob/master/setup.py
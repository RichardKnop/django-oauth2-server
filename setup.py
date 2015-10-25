from distutils.core import setup

setup(
    name='django-oauth2-server',
    version='0.0.1',
    packages=[
        'oauth2server',
    ],
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        'bcrypt==2.0.0',
        'cffi==1.3.0',
        'Django==1.8.5',
        'djangorestframework==3.2.4',
        'funcsigs==0.4',
        'mock==1.3.0',
        'passlib==1.6.5',
        'pbr==1.8.1',
        'psycopg2==2.6.1',
        'pycparser==2.14',
        'six==1.10.0',
        'wheel==0.24.0',
    ],
)

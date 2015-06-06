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
        'Django==1.8.2',
        'djangorestframework==3.1.1',
        'passlib==1.6.2',
        'psycopg2==2.5.1',
        'py-bcrypt==0.4',
        'wsgiref==0.1.2',
    ],
)

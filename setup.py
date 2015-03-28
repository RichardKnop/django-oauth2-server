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
        'Django==1.7.7',
        'djangorestframework==3.0.5',
        'passlib==1.6.2',
        'psycopg2==2.5.1',
        'py-bcrypt==0.4',
    ],
)

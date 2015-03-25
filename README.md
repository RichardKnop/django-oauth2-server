![Build Status](https://travis-ci.org/RichardKnop/django-oauth2-server.svg?branch=master)

Django OAuth2 Server
====================

Implementation of OAuth2 Server for Django (work in progress).

Installation
------------

Create a virtual environment:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install dependencies:

```
$ pip install -r requirements.txt
```

Create a local.py file and insert correct configuration details:

```
$ cp oauth2server/proj/settings/local.example.py oauth2server/proj/settings/local.py
$ nano cp oauth2server/proj/settings/local.py
```

Run the migrations:

```
$ python oauth2server/manage.py migrate
```

Running Tests
-------------

```
$ python oauth2server/manage.py test
```

Grant Types
===========

Client Credentials
------------------

Insert a test client:

```
insert into oauth_clients(id, client_identifier, client_secret, redirect_uri) values(1, 'testclient', '$2y$11$jDzY7PIFlO7zNYDud6WSkeujPLFo7B126Rbgx5UEZoPD8HoMBDhMK', '');
```

Run the development web server:

```
$ python oauth2server/manage.py runserver
```

And you can now get token either using HTTP Basic Authentication:

```
$ curl -u testclient:testpassword localhost:8080/api/v1/tokens/ -d 'grant_type=client_credentials'
```

Or using POST body:

```
$ curl localhost:8000/api/v1/tokens/ -d 'grant_type=client_credentials&client_id=testclient&client_secret=testpassword'
```

You should get a response like:

```json
{
    "access_token": "d4827dfdc325d4c23e9fca5dfe5ffea5d45fc9e9",
    "expires_in": 3600,
    "token_type": "Bearer",
    "scope": null
}
```

Authorization Code
------------------

Insert a test client:

```
insert into oauth_clients(id, client_identifier, client_secret, redirect_uri) values(1, 'testclient', '$2y$11$jDzY7PIFlO7zNYDud6WSkeujPLFo7B126Rbgx5UEZoPD8HoMBDhMK', '');
```

Run the development web server:

```
$ php -S localhost:8000 -t web web/index.php
```

And you can now go to this page in your web browser:

```
http://localhost:8000/authorize/?response_type=code&client_id=testclient&redirect_uri=https://www.example.com&state=somestate
```

You should see a screen like this:

![Authorization screen](https://github.com/JSainsburyPLC/jsid/blob/develop/images/authorization_screen.png)

Click yes, you will be redirected to the redirect_uri and the authorization code will be in the query string. For example:

```
https://www.example.com/?code=cd45169cf6575f76d789f55764cb751b4d08274d&state=somestate
```

You can use it to get access token:

```
$ curl -u testclient:testpassword localhost:8080/api/v1/tokens/ -d 'grant_type=authorization_code&code=cd45169cf6575f76d789f55764cb751b4d08274d'
```

You should get a response like:

```json
{
    "access_token": "1234f5adae8769978f64746176e7cdf37dc80ae0",
    "expires_in": 3600,
    "token_type": "Bearer",
    "scope": null,
    "refresh_token": "37f723616531afda7dde38be361b9a315238bd9b"
}
```

User Credentials
----------------

Insert a test client:

```
insert into oauth_clients(id, client_identifier, client_secret, redirect_uri) values(1, 'testclient', '$2y$11$jDzY7PIFlO7zNYDud6WSkeujPLFo7B126Rbgx5UEZoPD8HoMBDhMK', '');
```

Insert a test user:

```
insert into oauth_users(id, email, password) values(1, 'testuser@example.com', '$2y$11$jDzY7PIFlO7zNYDud6WSkeujPLFo7B126Rbgx5UEZoPD8HoMBDhMK');
```

And you can now get a new access token:

```
$ curl -u testclient:testpassword localhost:8080/api/v1/tokens/ -d 'grant_type=password&username=testuser@example.com&password=testpassword'
```

You should get a response like:

```json
{
    "access_token": "673d6c58f9dc87f14a5f0cecd986d1ba78dda3a9",
    "expires_in": 3600,
    "token_type": "Bearer",
    "scope": null,
    "refresh_token": "55697efd4b74c980f2c638602556115bc14ca931"
}
```

Refresh Token
-------------

Let's say you have created a new access token using the user credentials grant type. The response included a refresh token which you can use to get a new access token before your current access token expires.

```
$ curl -u testclient:testpassword localhost:8080/api/v1/tokens/ -d 'grant_type=refresh_token&refresh_token=55697efd4b74c980f2c638602556115bc14ca931'
```

And you get a new access token:

```json
{
    "access_token": "bbd07e78ace597a681f85ede3daee174a9e0703c",
    "expires_in": 3600,
    "token_type": "Bearer",
    "scope": null,
    "refresh_token":"5756f4fde22a0accf78279f8fd64258f22539dc4"
}
```

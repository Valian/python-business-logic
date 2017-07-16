=============================
Django Application Logic
=============================

.. image:: https://badge.fury.io/py/django-application-logic.svg
    :target: https://badge.fury.io/py/django-application-logic

.. image:: https://travis-ci.org/Valian/django-application-logic.svg?branch=master
    :target: https://travis-ci.org/Valian/django-application-logic

.. image:: https://codecov.io/gh/Valian/django-application-logic/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Valian/django-application-logic

Django package that makes creating complicated business logic easy

Documentation
-------------

The full documentation is at https://django-application-logic.readthedocs.io.

Quickstart
----------

Install Django Application Logic::

    pip install django-application-logic

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_application_logic.apps.DjangoApplicationLogicConfig',
        ...
    )

Add Django Application Logic's URL patterns:

.. code-block:: python

    from django_application_logic import urls as django_application_logic_urls


    urlpatterns = [
        ...
        url(r'^', include(django_application_logic_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

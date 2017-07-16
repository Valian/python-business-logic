=====
Usage
=====

To use Django Application Logic in a project, add it to your `INSTALLED_APPS`:

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

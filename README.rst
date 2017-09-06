=====================
Python Business Logic
=====================

.. image:: https://badge.fury.io/py/python-business-logic.svg
    :target: https://badge.fury.io/py/python-business-logic

.. image:: https://travis-ci.org/Valian/python-business-logic.svg?branch=master
    :target: https://travis-ci.org/Valian/python-business-logic

.. image:: https://codecov.io/gh/Valian/python-business-logic/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Valian/python-business-logic

Python package that makes creating complicated business logic easy. Currently under development.

Documentation
-------------

The full documentation is at https://python-business-logic.readthedocs.io. (WIP)

Installation
------------

Install Python Business Logic::

    pip install python-business-logic

Getting Started
---------------

Core element of library are validators, functions that are created to ensure logic is correct::

.. code:: python

   >>> from business_logic.core import validator

   >>> @validator
   ... def can_watch_movie(user, movie):
   ...     # some example business logic, it can be as complex as you want
   ...     return user.is_parent or user.age >= movie.age_restriction


With validators you can decorate actions performed that will be checked against that validator::

.. code:: python

    >>> from business_logic.core import validated_by

    >>> @validated_by(can_watch_movie)
    ... def watch_movie(user, movie):
    ...     print("'{}' is watching movie '{}'".format(user.name, movie.name))


As you can see, arguments to validator must match those passed to function.
Now every call to `watch_movie` will require that validator `can_watch_movie` passes::

.. code:: python
    >>> import collections
    >>> User = collections.namedtuple('User', ['name', 'age', 'is_parent'])
    >>> Movie = collections.namedtuple('Movie', ['name', 'age_restriction'])
    >>> alice = User('Alice', 32, True)
    >>> bob = User('Bob', 6, False)
    >>> cartoon = Movie('Tom&Jerry', 0)
    >>> horror = Movie('Scream', 18)


    >>> watch_movie(bob, cartoon)
    'Bob' is watching movie 'Tom&Jerry'
    >>> watch_movie(alice, horror)
    'Alice' is watching movie 'Scream'
    >>> watch_movie(bob, horror) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "business_logic/core.py", line 48, in wrapper
        raise ServiceException("Validation failed!")
    business_logic.exceptions.LogicException: Validation failed!



You can skip validation using `validate=False`::

.. code:: python
    >>> watch_movie(user=bob, movie=horror, validate=False)
    'Bob' is watching movie 'Scream'


Also, if we just want to know if action is permitted, just let's run::

.. code:: python
    >>> validation = can_watch_movie(bob, horror, raise_exception=False)
    >>> validation
    <PermissionResult success=False error=Validation failed!>
    >>> bool(validation)
    False
    >>> validation.error  # it's actual exception
    LogicException('Validation failed!',)



Chaining validators is really easy and readable::

.. code:: python
   >>> @validator
   ... def is_old_enough(user, movie):
   ...     return user.age >= movie.age_restriction

   >>> @validator
   ... def can_watch_movie(user, movie):
   ...     is_old_enough(user, movie)
   ...     # we don't have to return anything, @validator use exceptions

   >>> can_watch_movie(bob, horror)  # doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
      File "business_logic/core.py", line 48, in wrapper
        raise LogicException("Validation failed!")
   business_logic.exceptions.LogicException: Validation failed!



Ok, but we're still missing something. We don't know why exactly validation failed,
all we have is a generic "Validation failed!" message. How to fix that? It's easy, let's
make our own errors!

.. code:: python
   >>> from business_logic import LogicErrors, LogicException
   >>> class AgeRestrictionErrors(LogicErrors):
   ...     CANT_WATCH_MOVIE_TOO_YOUNG = LogicException("User is too young to watch this")

   >>> @validator
   ... def is_old_enough(user, movie):
   ...     if user.age < movie.age_restriction:
   ...          raise AgeRestrictionErrors.CANT_WATCH_MOVIE_TOO_YOUNG

   >>> is_old_enough(bob, horror)  # doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
   business_logic.exceptions.LogicException: User is too young to watch this

   >>> # we can also obtain exception details like this
   >>> result = is_old_enough(bob, horror, raise_exception=False)
   >>> bool(result)
   False
   >>> result.error
   LogicException('User is too young to watch this',)
   >>> result.error_code == 'CANT_WATCH_MOVIE_TOO_YOUNG'
   True
   >>> # result.errors is shortcut to registry with all errors
   >>> result.error == result.errors['CANT_WATCH_MOVIE_TOO_YOUNG']
   True


Testing is really easy:

.. code:: python
   >>> def test_user_cant_watch_movie_if_under_age_restriction():
   ...    bob = User('Bob', 6, False)
   ...    horror = Movie('Scream', 18)
   ...    result = can_watch_movie(bob, horror, raise_exception=False)
   ...    assert result.error_code == 'CANT_WATCH_MOVIE_TOO_YOUNG'

   >>> test_user_cant_watch_movie_if_under_age_restriction()



Usage
-----

When using this package, you should write all your business logic as simple functions, using only
inputs and Database Layer (for example, `Django ORM or SQLAlchemy`). This way, you can easily test your
logic and use it in any way you like. Convention that I follow is to put all functions inside `logic.py` file or `logic` submodule.

In **views** and **API** calls: Your role is to prepare all required data for business function (from forms, user session etc), call function
and present results to user. Middleware catching LogicException and, for example, displaying message to user in a generic way
can improve readability a lot, because no exception handling need to be done in view.

As **management commands**: In Django you can create custom `management command`, that allows you to use cli to perform custom logic.
Python Business Logic functions works very well with this use case!

From **external code**: Just import your function and use it. Since there shouldn't be any framework-related
inputs other than Database Models, usage is really simple. In reality, your business functions form **business API** of your application.


Running Tests
-------------

Does the code actually work?

::

    $ pip install -r requirements_test.txt
    $ tox

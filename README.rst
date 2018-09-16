=====================
Python Business Logic
=====================

.. image:: https://badge.fury.io/py/python-business-logic.svg
    :target: https://badge.fury.io/py/python-business-logic

.. image:: https://travis-ci.org/Valian/python-business-logic.svg?branch=master
    :target: https://travis-ci.org/Valian/python-business-logic

.. image:: https://codecov.io/gh/Valian/python-business-logic/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Valian/python-business-logic

.. image:: https://readthedocs.org/projects/python-business-logic/badge/?version=latest
    :target: http://python-business-logic.readthedocs.io


Traditionally, most web applications are written using MVC pattern. Python Business Logic helps you to add *Business Layer*, also called *Application Layer*, that is dependent only on models and composed of simple functions. Code written this way is extremely easy to read, test, and use in different scenarios. Package has no dependencies and can be used in any web framework, like Django, Flask, Bottle and others.

Documentation
-------------

The full documentation is at https://python-business-logic.readthedocs.io. Still under development. 

Installation
------------

Install Python Business Logic::

    pip install python-business-logic


Getting Started
---------------

Core elements of library are validators, functions created to ensure that business logic is correct:

.. code:: python

    >>> from business_logic.core import validator

    >>> @validator
    ... def can_watch_movie(user, movie):
    ...     # some example business logic, it can be as complex as you want
    ...     return user.is_parent or user.age >= movie.age_restriction



With validators you can decorate actions performed that will be checked against that validator:

.. code:: python

    >>> from business_logic.core import validated_by

    >>> @validated_by(can_watch_movie)
    ... def watch_movie(user, movie):
    ...     print("'{}' is watching movie '{}'".format(user.name, movie.name))



As you can see, arguments to validator must match those passed to function.
Now every call to :code:`watch_movie` will require that validator :code:`can_watch_movie` passes:

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


You can skip validation using :code:`validate=False`:

.. code:: python

    >>> watch_movie(user=bob, movie=horror, validate=False)
    'Bob' is watching movie 'Scream'



Also, if we just want to know if action is permitted, just let's run:

.. code:: python

    >>> validation = can_watch_movie(bob, horror, raise_exception=False)
    >>> validation
    <PermissionResult success=False error=Validation failed!>
    
    >>> bool(validation)
    False
    
    >>> validation.error  # it's an actual exception
    LogicException('Validation failed!',)



Chaining validators is really easy and readable:

.. code:: python

   >>> @validator
   ... def is_old_enough(user, movie):
   ...     return user.age >= movie.age_restriction

   >>> @validator
   ... def can_watch_movie(user, movie):
   ...     is_old_enough(user, movie)
   ...     # we don't have to return anything, @validator makes use of exceptions

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
   ...    result = is_old_enough(bob, horror, raise_exception=False)
   ...    # There are two ways to check if expected exceptions was raised
   ...    assert result.error_code == 'CANT_WATCH_MOVIE_TOO_YOUNG'
   ...    assert result.error == AgeRestrictionErrors.CANT_WATCH_MOVIE_TOO_YOUNG

   >>> test_user_cant_watch_movie_if_under_age_restriction()


Also, if you need to display parametrizable error messages, just use `.format` method

.. code:: python
   >>>
   >>> exc = LogicException('User {user} is way too young!', error_code='TOO_YOUNG')
   >>> formatted_exc = exc.format(user='Bob')
   >>> assert str(formatted_exc) == 'User Bob is way too young!'
   >>> assert exc.error_code == formatted_exc.error_code
   >>> assert exc == formatted_exc

Usage
-----

When using this package, you should write all your business logic as simple functions, using only
inputs and Database Layer (eg. `Django ORM or SQLAlchemy`). This way, you can easily test your
logic and use it in any way you like. Convention that I follow is to put all functions inside `logic.py` file or `logic` submodule.

In **views** and **API** calls: Your role is to prepare all required data for business function (from forms, user session etc), call function
and present results to user. Middleware catching LogicException and, for example, displaying message to user in a generic way
can improve readability a lot, because no exception handling need to be done in view.

As **management commands**: In Django you can create custom `management command`, that allows you to use cli to perform custom logic.
Python Business Logic functions works very well for that use case!

From **external code**: Just import your function and use it. Since there shouldn't be any framework-related
inputs other than Database Models, usage is really simple. In reality, your business functions form *business API* of your application.

Examples
--------

For examples how to use this library, look into directory *examples*. Currently there is only one called *Football match*. Most important file there is :code:`logic.py`.


Running Tests
-------------

Does the code actually work?

::

    $ pip install -r requirements_test.txt
    $ tox

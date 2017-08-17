=============================
Python Business Logic
=============================

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

```python
   >>> from business_logic.core import validator

   >>> @validator
   ... def can_remove_user(by_user, user):
   ...     return by_user.id == user.id or by_user.is_admin
```
With validators you can decorate actions performed that will be checked against that validator::

```python
    >>> from business_logic.core import validated_by

    >>> @validated_by(can_remove_user)
    ... def remove_user(by_user, user):
    ...     user.delete()
```

Now every call to `remove_user` will require that validator `can_remove_user` passes::

```python
    >>> import collections
    >>> User = collections.namedtuple('User', ['id', 'is_admin'])
    >>> alice = User(1, False)
    >>> bob = User(2, False)

    >>> remove_user(user=alice, by_user=bob) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "<doctest README.rst[8]>", line 1, in <module>
        remove_user(user=alice, by_user=bob)
      File "business_logic/core.py", line 23, in wrapper
        validation_func(raise_exception=True, *args, **kwargs)
      File "business_logic/core.py", line 48, in wrapper
        raise ServiceException("Validation failed!")
    business_logic.exceptions.LogicException: Validation failed!
```

Running Tests
-------------

Does the code actually work?

::

    $ pip install -r requirements_test.txt
    $ tox

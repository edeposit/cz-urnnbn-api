#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class KwargObj(object):
    """
    This class defines method to map kwargs to attributes, so you can just
    call :meth:`_kwargs_to_attributes` in your ``__init__``.

    For example::

        class Xex(object):
            def __init__(self, something, **kwargs):
                self.something = something
                self.something_else = None
                self.something_different = None

                self._kwargs_to_attributes(kwargs)

    This will allow to pass parameters which sets also ``something_else`` and
    ``something_different``.

    There is also modified :meth:`__setattr__`` method, which disables to set
    new attributes. This may be good idea for data containers and typos.

    Modified :meth:`__setattr__` functionality can be triggered by setting the
    ``_all_set`` attribute::

        class Xex(object):
            def __init__(self):
                self.something = None
                self.something_else = None
                self.something_different = None

                self._all_set = True

    It will be now impossible to create new attribute, which may be good for
    handling typos. You can still redefine already defined attributes!
    """
    def __setattr__(self, name, value):
        """
        Disable setting values which are not defined in ``.__init__()``.
        """
        if hasattr(self, "_all_set") and name not in self.__dict__:
            raise ValueError("%s is not defined in this class!" % name)

        self.__dict__[name] = value

    def _kwargs_to_attributes(self, kwargs):
        """
        Put keys from `kwargs` to `self`, if the keys are already there.
        """
        for key, val in kwargs.iteritems():
            if key not in self.__dict__:
                raise ValueError(
                    "Can't set %s parameter - it is not defined here!" % key
                )

            self.__dict__[key] = val

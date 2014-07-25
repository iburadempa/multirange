multirange
==========

Convenience functions for multiple range objects with step == 1

An elementary package for Python >= 3.3

https://pypi.python.org/pypi/multirange/

Status
------

The code works, but it is not stable: functionality might be added
or reorganized. Stability grows when I get feedback, or - but much
slower - when just I use it and time passes by.

Introduction
------------

This library for Python >= 3.3 provides convenience functions for multiple
range objects with step == 1 (corresponding to finite sets of consecutive
integers).

It has 3 types of operations:

    * operations involving few range objects
    * operations involving an iterable of range objects (*range iterable*)
    * operations involving so-called multiranges; we define a *multirange*
      as an iterable of ranges, which have no mutual overlap, which are not
      adjacent, and which are ordered increasingly;
      a special case of multirange is a *partition* of finite set of
      consecutive integers

It is not yet feature complete; most operations involving multiranges are
missing.

Examples
--------

::

  >>> import multirange as mr
  >>> mr.intermediate(range(10, 15), range(0, 5))

  range(5, 10)

  >>> list(mr.gaps([range(4, 6), range(6, 7), range(8, 10), range(0, 1), range(1, 3)]))

  [range(3, 4), range(7, 8)]

  >>> mr.difference(range(1, 9), range(2, 3))

  (range(1, 2), range(3, 9))

  >>> mr.normalize_multi([None, range(0, 5), range(5, 7), range(8, 20)])

  [range(0, 7), range(8, 20)]

Consult the unit tests for more examples.

Documentation
-------------

https://multirange.readthedocs.org

Source
------

https://github.com/iburadempa/multirange

See also
--------

If *multirange* is not what you are searching for, you might
be interested in one of these python modules:

 * rangeset_
 * intspan_
 * cowboy_

.. _rangeset: https://pypi.python.org/pypi/rangeset
.. _intspan: https://pypi.python.org/pypi/intspan
.. _cowboy: https://pypi.python.org/pypi/cowboy

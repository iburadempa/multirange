multirange
==========
Convenience functions for multiple range objects with step == 1

An elementary package for Python >= 3.3

https://pypi.python.org/pypi/multirange/

Status
------
The code works, but it is not stable: functionality might be added
or reorganized as long as the major version equals 0
(cf. http://semver.org/spec/v2.0.0.html, item #4).
Hint: Stability grows quicker when you provide feedback.

multirange is not yet feature complete; most operations involving
multiranges are missing.

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

Examples
--------
::
    >>> import multirange as mr
    >>> mr.normalize(range(5, 0))
    >>> mr.overlap(range(0, 10), range(5, 15))
    range(5, 10)
    >>> mr.is_disjunct([range(8, 10), range(0, 2), range(2, 4)])
    True
    >>> mr.covering_all([range(8, 10), range(0, 2), range(2, 4)])
    range(0, 10)
    >>> mr.contains(range(0, 10), range(0, 5))
    True
    >>> mr.is_covered_by([range(8, 10), range(0, 2)], range(0, 20))
    True
    >>> mr.intermediate(range(10, 15), range(0, 5))
    range(5, 10)
    >>> list(mr.gaps([range(4, 6), range(6, 7), range(8, 10), range(0, 3)]))
    [range(3, 4), range(7, 8)]
    >>> mr.difference(range(1, 9), range(2, 3))
    (range(1, 2), range(3, 9))
    >>> list(mr.normalize_multi([None, range(0, 5), range(5, 7), range(8, 20)]))
    [range(0, 7), range(8, 20)]
    >>> list(mr.difference_one_multi(range(0, 10), [range(-2, 2), range(4, 5)]))
    [range(2, 4), range(5, 10)]

Please consult the unit tests for more examples.

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
 * cs.range_

.. _rangeset: https://pypi.python.org/pypi/rangeset
.. _intspan: https://pypi.python.org/pypi/intspan
.. _cowboy: https://pypi.python.org/pypi/cowboy
.. _cs.range: https://pypi.python.org/pypi/cs.range


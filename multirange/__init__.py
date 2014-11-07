# -*- coding: utf-8 -*-

# Copyright (C) 2014 ibu@radempa.de
#
# Permission is hereby granted, free of charge, to
# any person obtaining a copy of this software and
# associated documentation files (the "Software"),
# to deal in the Software without restriction,
# including without limitation the rights to use,
# copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is
# furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission
# notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
# OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
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

Features
~~~~~~~~

    * provide operations on multiple instances of *range*
      (considered having *step* == 1)

      .. note::

        Since Python 3.3 *range* objects have the *start*, *stop* and *step*
        attributes.

    * avoid materializing of ranges as lists.
      Instead, the boundaries (start, stop) are used to calculate results.
    
    * if not otherwise noted, the functions of this module throw no Exceptions,
      provided they are called with valid parameters.

Limitations
~~~~~~~~~~~

    * Requires Python >= 3.3

Range
~~~~~

A ``range(l, m)`` thus has the meaning of a set of all consecutive integers
from l to m - 1. If l >= m, this means the empty set. Note that for negative
step values the native range object may generate several values, while our
range object may be emtpy. Example: range(0, -10, -1) generates
10 values, while in our view it is empty.

In its normalized form (cf. :func:`normalize`) a range (1) has step == 1 and
(2) has either l < m, or is None.

The functions of this module always accept ranges in their normalized form,
and if not otherwise stated, non-normalized ranges are accepted, too.

Range iterable
~~~~~~~~~~~~~~

The purpose of this module is to ease common operations involving
multiple ranges, i.e., iterables of ranges. By *range iterable*
we mean an iterable yielding either None or an instance of :py:obj:`range`.

.. warning::

    Some functions need to sort range iterables, thereby defining
    an intermediate list, so don't expect performance for iterables
    with a large number of items for all functions.

Range iterables are not to be confused with multiranges.

Multirange
~~~~~~~~~~

As *multirange* we define a range iterable where the ranges don't
overlap, are not adjacent and are ordered increasingly.

Usage examples
--------------

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

Functions
---------

"""

__version__ = (0, 1, 3)

def normalize(r):
    """
    Return an object which is the normalizion of range *r*
    
    The normalized range is either None (if r.start >= r.stop), or equals to
    range(r.start, r.stop, 1).
    """
    if isinstance(r, range):
        if r.stop <= r.start:
            return None
        else:
            if r.step == 1:
                return r
            else:
                return range(r.start, r.stop)
    else:
        return None

def filter_normalize(rs):
    """
    Iterate over all ranges in the given range iterable *rs*, yielding
    normalized ranges
    """
    for r in rs:
        yield normalize(r)

def filter_nonempty(rs, invert=False, do_normalize=True, with_position=False):
    """
    Iterate over all ranges in the given range iterable *rs* and yield those
    which are not None after normalization; if *invert* is True, yield those
    which are None

    If *do_normalize* is True, yield only normalized non-empty ranges;
    otherwise yield the original ranges.

    If with_position is True, return 2-tuples consisting of the position of
    the matching range within *rs* and the matching range. Otherwise yield
    only the matching range.
    """
    for pos, r in enumerate(rs):
        n = normalize(r)
        if (not invert and n is not None) or (invert and n is None):
            if do_normalize:
                if with_position:
                    yield pos, n
                else:
                    yield n
            else:
                if with_position:
                    yield pos, r
                else:
                    yield r

def equals(r1, r2):
    """
    Return whether the the two ranges *r1* and *r2* are equal after
    normalization

    Note: If you don't have None values and want to take into accoutn the
    step values, you can use native python equality of ranges; for instance,
    range(0, 5, -10) = range(0, -5) == range(0).
    """
    n1 = normalize(r1)
    n2 = normalize(r2)
    if n1 is None:
        return n2 is None
    return n1 == n2

def filter_equal(rs, r, with_position=False):
    """
    Iterate over all ranges in the given range iterable *rs* and yield those
    which are equal to range *r* after normalization, together with their
    position within *rs*

    Yield 2-tuples consisting of an :py:obj:`int` indicating the position
    within *rs* and a normalized range.
    """
    r = normalize(r)
    for pos, r1 in enumerate(rs):
        n1 = normalize(r1)
        if equals(n1, r):
            if with_position:
                yield pos, n1
            else:
                yield n1

def overlap(r1, r2):
    """
    For two ranges *r1* and *r2* return the normalized range corresponding to
    the intersection ot the sets (of consecutive integers) corresponding to
    *r1* and *r2*

    Return a normalized result.
    """
    if r1 is None or r1.stop <= r1.start:
        return None
    if r2 is None or r2.stop <= r2.start:
        return None
    if r1.stop <= r2.start or r2.stop <= r1.start:
        return None
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))

def filter_overlap(rs, r, with_position=False):
    """
    Iterate over the range iterable *rs*, and yield only those ranges
    having a non-vanishing overlap with range *r*
    
    Some of the original ranges are yielded, not their overlapping parts.
    """
    for pos, r1 in enumerate(rs):
        if overlap(r1, r):
            if with_position:
                yield pos, r1
            else:
                yield r1

def match_count(rs, r):
    """
    Return the number of ranges yielded from iterable *rs*,
    which have a non-vanishing overlap with range *r*
    """
    n = 0
    for r2 in rs:
        if overlap(r, r2):
            n += 1
    return n

def overlap_all(rs):
    """
    Return the range corresponding to the intersection of the sets of integers
    corresponding to the ranges obtained from the iterable *rs*

    Return a normalized result.
    """
    brk = False
    o = None
    for r in rs:
        if brk is False:
            o = normalize(r)
            brk = True
        else:
            if o is None:
                return None
            o = overlap(o, r)
    return o

def is_disjunct(rs, assume_ordered_increasingly=False):
    """
    Return whether the range iterable *rs* consists of mutually disjunct ranges

    If *assume_ordered_increasingly* is True, only direct neighbors (qua
    iteration order) are checked for non-vanishing overlap.
    """
    if not assume_ordered_increasingly:
        rs = sorted(filter_nonempty(rs), key=lambda x: x.start)
    left = None
    for right in rs:
        if left is not None and overlap(left, right):
            return False
        left = right
    return True

def covering_all(rs):
    """
    Return the smallest covering range for the ranges in range iterable *rs*

    Return a normalized result.
    """
    l_c = None
    m_c = None
    for s in rs:
        s1 = normalize(s)
        if s1 is not None:
            if l_c is not None:
                l, m = s1.start, s1.stop
                l_c = min(l_c, l)
                m_c = max(m_c, m)
            else:
                l_c, m_c = s1.start, s1.stop
    if l_c is None:
        return None
    return range(l_c, m_c)

def contains(r1, r2):
    """
    Return whether range *r1* contains range *r2*
    """
    n1 = normalize(r1)
    n2 = normalize(r2)
    if n2 is None:
        return True
    if n1 is None:
        return False # n2 is not None
    l1, m1 = n1.start, n1.stop
    l2, m2 = n2.start, n2.stop
    if l1 <= l2 and m2 <= m1:
        return True
    return False

def filter_contained(rs, r, with_position=False):
    """
    Yield those ranges from range iterable *rs*, which are contained in range
    *r*

    If with_position is True, yield 2-tuples consisting of the position of the
    matching range within *rs* and the matching range.
    """
    for pos, r1 in enumerate(rs):
        if contains(r, r1):
            if with_position:
                yield pos, r1
            else:
                yield r1

def is_covered_by(rs, r):
    """
    Return whether range *r* covers all ranges from range iterable *rs*
    """
    cov = covering_all(rs)
    return contains(r, cov)

def intermediate(r1, r2, assume_ordered=False):
    """
    Return the range inbetween range *r1* and range *r2*, or None
    if they overlap or if at least one of them corresponds to an empty set

    Return a normalized result.
    """
    n1 = normalize(r1)
    n2 = normalize(r2)
    if n1 is None:
        return None
    if n2 is None:
        return None
    l1, m1 = n1.start, n1.stop
    l2, m2 = n2.start, n2.stop
    if m1 < l2:
        return range(m1, l2)
    if not assume_ordered and m2 < l1:
        return range(m2, l1)
    return None

def sort_by_start(rs):
    """
    Return a list of normalized ranges in the range iterable *rs*,
    sorted by their start values, and omitting empty ranges
    """
    rs = [s for s in rs if normalize(s) is not None]
    return sorted(rs, key=lambda x: x.start)

def gaps(rs, assume_ordered=False):
    """
    Yield the gaps between the ranges from range iterable *rs*, i.e.,
    the maximal ranges without overlap with any of the ranges, but within
    the covering range

    Yield normalized, non-empty ranges.
    """
    if not assume_ordered:
        rs = sort_by_start(rs)
    l = None # last seen lower end
    m = None # maximum of upper end within the set of ranges with lower end l
    for r_next in rs:
        r_next = normalize(r_next)
        if r_next is not None:
            #print((l, m), r_next)
            if l is not None:
                im = intermediate(range(l, m), r_next)
                if im is not None:
                    yield im
                l1, m1 = r_next.start, r_next.stop
                if l == l1:
                    m = max(m, m1)
                else:
                    l = l1
                    m = m1
            else:
                l, m = r_next.start, r_next.stop

def is_partition_of(rs, assume_ordered=False):
    """
    Return the covering range of the ranges from range iterable *rs*,
    if they have no gaps; else return None
    """
    for s in gaps(rs, assume_ordered=assume_ordered):
        if s is not None:
            return None
    return covering_all(rs)

def difference(r1, r2):
    """
    Return two ranges resulting when the integers from range *r2* are
    removed from range *r1*

    Return two ranges: the first being the part below *r2* and the second
    the one above *r2*. They may both be None. In the special case where *r2*
    after normalization equals None, return (r1, None) (i.e., take the
    difference to be the lower part).
    """
    n1 = normalize(r1)
    n2 = normalize(r2)
    if n1 is None:
        return None, None
    if n2 is None:
        return r1, None
    m1, l1 = r1.start, r1.stop
    m2, l2 = r2.start, r2.stop
    if m1 < m2:
        below = range(m1, min(l1, m2))
    else:
        below = None
    if l2 < l1:
        above = range(max(m1, l2), l1)
    else:
        above = None
    return below, above

def normalize_multi(rs, assume_ordered_increasingly=False):
    """
    Return a multirange from the given range iterable *rs*
    
    Overlapping or adjacent ranges are merged into one, and the ranges are
    ordered increasingly.
    
    Yield normalized ranges. Don't yield None.
    """
    if not assume_ordered_increasingly:
        rs = sorted(filter_nonempty(rs), key=lambda x: x.start)
    l = None    # last seen lower end of the range to be emitted
    m = None    # upper end of the current group of overlapping ranges
    last = None # last seen range
    for r_next in filter_nonempty(rs):
        if l is not None:
            l1, m1 = r_next.start, r_next.stop
            if l1 > m:
                yield range(l, m)
                l, m = l1, m1 # for the next iteration
                last = r_next  # if there is no next iteration
            else:
                m = max(m, m1)     # for the next iteration
                last = range(l, m) # if there is no next iteration
        else:
            l, m = r_next.start, r_next.stop
            last = range(l, m)
    if last is not None:
        yield last

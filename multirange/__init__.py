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
Convenience functions for multiple range-like objects

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

Overview
~~~~~~~~
This library for Python >= 3.3 provides convenience functions for multiple
range-like objects corresponding to finite sets of consecutive integers.

It has 3 main types of operations:

    * operations involving few range-like objects (a generalization of Python's
      native range objects)
    * operations involving an iterable of range-like objects (*range iterables*)
    * operations involving so-called multiranges; we define a *multirange*
      as iterables range-like objects, which have no mutual overlap, which
      are not adjacent, and which are ordered increasingly; a special case
      of multirange corresponds to a *partition* of a finite set of consecutive
      integers.

Features
~~~~~~~~
    * Provide operations on multiple instances of *range*
      (disregarding attribute *step*), or any other object having attributes
      *start* and *stop* evaluating to :py:obj:`int`

      .. note::

        Since Python 3.3 :py:obj:`range` objects have the *start*, *stop* and
        *step* attributes.

    * Avoid materializing of ranges as full lists of integers.
      Instead, results are computed from the boundaries (start, stop) only.

    * If not otherwise noted, the functions of this module throw no Exceptions,
      provided they are called with valid parameters.

Limitations
~~~~~~~~~~~
    * Require Python >= 3.3

Range
~~~~~
In the context of this module we define as a *range* *r* either a native Python
:py:obj:`range` object, or any other object having attributes *start* and
*stop*, which evaluate to :py:obj:`int`.

A range *r* has the meaning of the set of all consecutive integers from r.start
to r.stop - 1. If r.start >= r.stop, this means the empty set.
Note that for negative step values the native Python :py:obj:`range` object
may generate several values, while in our context an empty set may result.
Example: range(0, -10, -1) generates 10 values, while in our context (step == 1)
this entails an empty set of integers.

Ranges often need to be brought to normal form (cf. :func:`normalize`).
By default the normal form is a native :py:obj:`range` object with step == 1,
or None if r.stop <= r.start. Alternatively, in case r.stop > r.start, the
normal form may be any other *generalized range object*, which is obtained
using a non-default value of the *construct* keyword argument in most functions
(see below).

The functions of this module always accept ranges in their normalized form,
and if not otherwise stated, non-normalized ranges are accepted, too.

Generalized range object
~~~~~~~~~~~~~~~~~~~~~~~~
When the documentation of this module refers to a *range*, it usually means
a *generalized range object*, not just Python's native :py:obj:`range`.

As *generalized range object* we define an object which can be constructed
using exactly two integer arguments, *start* and *stop*, and which has
attributes *start* and *stop* returning these integer values at any time.
One example is the native :py:obj:`range` object. Here is another very simple
one::

    class MyRange(object):
        def __init__(self, start, stop):
            self.start = start
            self.stop = stop

The main advantage of generalized range objects over native range objects is
that they may have additional structure beyond *start* and *stop* (where the
native range only has a *step* attribute).

Range iterable
~~~~~~~~~~~~~~
The purpose of this module is to ease common operations involving
multiple ranges, more precisely, iterables of ranges. By *range iterable*
we mean an iterable yielding either None or an instance of a generalized
range object.

.. warning::

    Some functions need to sort range iterables, thereby defining
    an intermediate list, so don't expect optimal performance for iterables
    with a large number of items for all functions.

Range iterables are not to be confused with multiranges.

Multirange
~~~~~~~~~~
As *multirange* we define a range iterable where the ranges don't
overlap, are not adjacent and are ordered increasingly. A *multirange*
can be obtained from any *range iterable* by using :func:`normalize_multi`.

Usage examples
--------------
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

Functions
---------
"""

__version__ = (0, 2, 0)

def normalize(r, construct=range):
    """
    Return an object which is the normalization of range *r*

    The normalized range is either None (if r.start >= r.stop), or an object
    constructed using *construct* with the arguments r.start, r.stop.

    In case construct == range we try to avoid constructing new objects.
    """
    if r is None:
        return None
    if r.stop <= r.start:
        return None
    else:
        if construct == range and isinstance(r, range) and r.step == 1:
            return r
        else:
            return construct(r.start, r.stop)

def filter_normalize(rs, construct=range):
    """
    Iterate over all ranges in the given range iterable *rs*, yielding
    normalized ranges
    """
    for r in rs:
        yield normalize(r, construct=construct)

def filter_nonempty(rs, invert=False, do_normalize=True, construct=range,
                    with_position=False):
    """
    Iterate over all ranges in the given range iterable *rs* and yield those
    which are not None after normalization; if *invert* is True, yield those
    which are None

    If *do_normalize* is True, yield only normalized non-empty ranges
    (using the constructor given in *construct* upon normalization);
    otherwise yield the original range objects.

    If with_position is True, return 2-tuples consisting of the position of
    the matching range within *rs* and the matching range. Otherwise yield
    only the matching range.
    """
    for pos, r in enumerate(rs):
        n = normalize(r, construct=construct)
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

    Incidental remark: If you have native range objects (being not None) and
    want to take into account step values, you can use native python equality
    of ranges; for instance, range(0, 5, -10) == range(0, -5) == range(0).
    """
    n1 = normalize(r1)
    n2 = normalize(r2)
    if n1 is None:
        return n2 is None
    return n1 == n2

def filter_equal(rs, r, do_normalize=True, construct=range,
                 with_position=False):
    """
    Iterate over all ranges in the given range iterable *rs* and yield those
    which are equal to range *r* after normalization

    If *do_normalize* evaluates to True, then do not return the original items
    from *rs*, but instead normalized ranges, where the range objects are
    constructed using *construct*.

    If *with_position* evalues to True, then yield 2-tuples consisting of an
    :py:obj:`int` indicating the position of a matching range within *rs* and
    the range itself.
    """
    n = normalize(r)
    for pos, r1 in enumerate(rs):
        n1 = normalize(r1, construct=construct)
        if (n1 is None and n is None) or (n1 is not None and n is not None
          and n1.start == n.start and n1.stop == n.stop):
            if with_position:
                yield pos, (n1 if do_normalize else r1)
            else:
                yield (n1 if do_normalize else r1)

def overlap(r1, r2, construct=range):
    """
    For two ranges *r1* and *r2* return the normalized range corresponding to
    the intersection ot the sets (of consecutive integers) corresponding to
    *r1* and *r2*

    Return a normalized result, which is either None, or an object constructed
    using *construct*.
    """
    if r1 is None or r1.stop <= r1.start:
        return None
    if r2 is None or r2.stop <= r2.start:
        return None
    if r1.stop <= r2.start or r2.stop <= r1.start:
        return None
    return construct(max(r1.start, r2.start), min(r1.stop, r2.stop))

def filter_overlap(rs, r, do_normalize=False, construct=range,
                   with_position=False):
    """
    Iterate over the range iterable *rs*, and yield only those ranges
    having a non-vanishing overlap with range *r*

    Note: Some of the original ranges are yielded, not their overlapping parts.

    If *do_normalize* evaluates to True, then do not return the original items
    from *rs*, but instead normalized range objects constructed using
    *construct*.

    If *with_position* evalues to True, then yield 2-tuples consisting of an
    :py:obj:`int` indicating the position of a matching range within *rs* and
    the range itself.
    """
    for pos, r1 in enumerate(rs):
        if overlap(r1, r) is not None:
            if with_position:
                yield pos, (normalize(r1, construct=construct)
                            if do_normalize else r1)
            else:
                yield (normalize(r1, construct=construct)
                       if do_normalize else r1)

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

def overlap_all(rs, construct=range):
    """
    Return the range corresponding to the intersection of the sets of integers
    corresponding to the ranges obtained from the iterable *rs*

    Return a normalized result, where the normalized object is constructed
    using *construct*.
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
    return normalize(o, construct=construct)

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

def covering_all(rs, construct=range):
    """
    Return the smallest covering range for the ranges in range iterable *rs*

    Return a normalized result, where the normalized object is constructed
    using *construct*.
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
    return construct(l_c, m_c)

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
    return n1.start <= n2.start and n2.stop <= n1.stop

def filter_contained(rs, r, do_normalize=False, construct=range,
                     with_position=False):
    """
    Yield those ranges from range iterable *rs*, which are contained in range
    *r*

    If *do_normalize* evaluates to True, then do not return the original items
    from *rs*, but instead normalized range objects constructed using
    *construct*.

    If *with_position* evalues to True, then yield 2-tuples consisting of an
    :py:obj:`int` indicating the position of a matching range within *rs* and
    the range itself.
    """
    for pos, r1 in enumerate(rs):
        if contains(r, r1):
            if with_position:
                yield pos, (normalize(r1, construct=construct)
                            if do_normalize else r1)
            else:
                yield (normalize(r1, construct=construct)
                       if do_normalize else r1)

def is_covered_by(rs, r):
    """
    Return whether range *r* covers all ranges from range iterable *rs*
    """
    cov = covering_all(rs)
    return contains(r, cov)

def intermediate(r1, r2, construct=range, assume_ordered=False):
    """
    Return the range inbetween range *r1* and range *r2*, or None
    if they overlap or if at least one of them corresponds to an empty set

    Return a normalized range object constructed using *construct*.
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
        return construct(m1, l2)
    if not assume_ordered and m2 < l1:
        return construct(m2, l1)
    return None

def sort_by_start(rs):
    """
    Return a list of (unmodified) ranges obtained from range iterable *rs*,
    sorted by their start values, and omitting empty ranges
    """
    rs = [s for s in rs if normalize(s) is not None]
    return sorted(rs, key=lambda x: x.start)

def gaps(rs, construct=range, assume_ordered=False):
    """
    Yield the gaps between the ranges from range iterable *rs*, i.e.,
    the maximal ranges without overlap with any of the ranges, but within
    the covering range

    Yield normalized, non-empty range objects constructed using *construct*.
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
                im = intermediate(range(l, m), r_next, construct=construct)
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

def is_partition_of(rs, construct=range, assume_ordered=False):
    """
    Return the covering range of the ranges from range iterable *rs*,
    if they have no gaps; else return None

    The covering range is constructed using *construct*.
    """
    for s in gaps(rs, assume_ordered=assume_ordered):
        if s is not None:
            return None
    return covering_all(rs, construct=construct)

def difference(r1, r2, construct=range):
    """
    Return two ranges resulting when the integers from range *r2* are
    removed from range *r1*

    Return two ranges: the first being the part below *r2* and the second
    the one above *r2*. They may both be None. In the special case where *r2*
    after normalization equals None, return (r1, None) (i.e., take the
    difference to be the lower part).

    The range objects are constructed using *construct*.
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
        below = construct(m1, min(l1, m2))
    else:
        below = None
    if l2 < l1:
        above = construct(max(m1, l2), l1)
    else:
        above = None
    return below, above

def normalize_multi(rs, construct=range, assume_ordered_increasingly=False):
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
                yield construct(l, m)
                l, m = l1, m1 # for the next iteration
                last = r_next # if there is no next iteration
            else:
                m = max(m, m1)         # for the next iteration
                last = construct(l, m) # if there is no next iteration
        else:
            l, m = r_next.start, r_next.stop
            last = construct(l, m)
    if last is not None:
        yield last

def difference_one_multi(r, mr, construct=range):
    """
    Subtract multirange *mr* from range *r*, resulting in a multirange

    The range objects of the yielded range iterable are construced using
    *construct*.
    """
    n = normalize(r)
    if n is None:
        return 
    l = n.start
    m = n.stop
    i = l
    for r1 in mr:
        if r1.start <= l:
            i = max(l, r1.stop)
            continue
        if r1.start >= m:
            yield construct(i, m)
            return
        yield construct(i, r1.start)
        i = r1.stop
    if i < m:
        yield construct(i, m)


# -*- coding: utf-8 -*-

import unittest

from multirange import *


class MyRange(object):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

class TestMultirange(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize(range(-1, 1)), range(-1, 1))
        self.assertEqual(normalize(range(1, 1)), None)
        self.assertEqual(normalize(range(1, -1)), None)
        self.assertEqual(normalize(None), None)
        self.assertEqual(normalize(MyRange(-1, 1)), range(-1, 1))
        myrange = normalize(MyRange(-1, 1), construct=MyRange)
        self.assertEqual(myrange.start, -1)
        self.assertEqual(myrange.stop, 1)
        myrange = normalize(MyRange(1, 1), construct=MyRange)
        self.assertEqual(myrange, None)
        myrange = normalize(MyRange(1, -1), construct=MyRange)
        self.assertEqual(myrange, None)
        myrange = normalize(None, construct=MyRange)
        self.assertEqual(myrange, None)

    def test_filter_normalize(self):
        rs = [range(0, -1, -1), range(1, 5, 2), range(7, 7)]
        self.assertEqual(list(filter_normalize(rs)), [None, range(1, 5), None])
        rs = [MyRange(0, -1), MyRange(1, 5), MyRange(7, 7)]
        self.assertEqual(list(filter_normalize(rs)), [None, range(1, 5), None])
        n = list(filter_normalize(rs, construct=MyRange))
        self.assertEqual(len(n), 3)
        self.assertEqual(n[0], None)
        self.assertTrue(isinstance(n[1], MyRange))
        self.assertEqual(n[1].start, 1)
        self.assertEqual(n[1].stop, 5)
        self.assertEqual(n[2], None)

    def test_filter_nonempty(self):
        rs = (range(0, 10), range(10, 10), range(5, -5), range(0, 10, 2))
        self.assertEqual(list(filter_nonempty(rs)), [range(0, 10), range(0, 10)])
        self.assertEqual(list(filter_nonempty(rs, do_normalize=False)), [range(0, 10), range(0, 10, 2)])
        self.assertEqual(list(filter_nonempty(rs, invert=True)), [None, None])
        self.assertEqual(list(filter_nonempty(rs, invert=True, do_normalize=False)), [range(10, 10), range(5, -5)])
        self.assertEqual(list(filter_nonempty(rs, with_position=True)), [(0, range(0, 10)), (3, range(0, 10))])
        self.assertEqual(list(filter_nonempty(rs, do_normalize=False, with_position=True)), [(0, range(0, 10)), (3, range(0, 10, 2))])
        self.assertEqual(list(filter_nonempty(rs, invert=True, with_position=True)), [(1, None), (2, None)])
        self.assertEqual(list(filter_nonempty(rs, invert=True, do_normalize=False, with_position=True)), [(1, range(10, 10)), (2, range(5, -5))])
        rs = [MyRange(0, 10), MyRange(10, 10), MyRange(5, -5), MyRange(0, 10)]
        self.assertEqual(list(filter_nonempty(rs)), [range(0, 10), range(0, 10)])
        ne = list(filter_nonempty(rs, construct=MyRange))
        self.assertEqual(len(ne), 2)
        self.assertTrue(isinstance(ne[0], MyRange))
        self.assertEqual(ne[0].start, 0)
        self.assertEqual(ne[0].stop, 10)
        self.assertTrue(isinstance(ne[1], MyRange))
        self.assertEqual(ne[1].start, 0)
        self.assertEqual(ne[1].stop, 10)

    def test_equal(self):
        self.assertEqual(equals(None, None), True)
        self.assertEqual(equals(range(0, 7, 3), range(0, 7, 3)), True)
        self.assertEqual(equals(range(0, 7, 3), range(0, 7, 4)), True)
        self.assertEqual(equals(range(0, 7, 3), range(0, 7)), True)
        self.assertEqual(equals(range(0, 5, 3), range(0, 3, 3)), False)
        self.assertEqual(equals(range(0, 5, 3), range(0, 4, 3)), False)
        self.assertEqual(equals(range(0, 0), None), True)
        self.assertEqual(equals(range(0, 10, 100), range(0, 1)), False)
        self.assertEqual(equals(range(0, -1), None), True)

    def test_filter_equal(self):
        rs = [range(0, 1), range(0, 2, 3), None, range(-1, -5, -3), range(0, 2)]
        self.assertEqual(list(filter_equal(rs, range(0, 2))), [range(0, 2), range(0, 2)])
        self.assertEqual(list(filter_equal(rs, None)), [None, None])
        self.assertEqual(list(filter_equal(rs, range(0, 2), with_position=True)), [(1, range(0, 2)), (4, range(0, 2))])
        self.assertEqual(list(filter_equal(rs, None, with_position=True)), [(2, None), (3, None)])
        self.assertEqual(list(filter_equal(rs, range(0, 2), do_normalize=False)), [range(0, 2, 3), range(0, 2)])
        self.assertEqual(list(filter_equal(rs, range(0, 2), do_normalize=False, with_position=True)), [(1, range(0, 2, 3)), (4, range(0, 2))])
        rs = [range(0, 1), MyRange(0, 2), MyRange(-1, -5), range(0, 2, 5)]
        fe = list(filter_equal(rs, range(0, 2, 10)))
        self.assertEqual(fe, [range(0, 2), range(0, 2)])
        fe = list(filter_equal(rs, MyRange(0, 2)))
        self.assertEqual(fe, [range(0, 2), range(0, 2)])
        fe = list(filter_equal(rs, range(0, 2, 5), construct=MyRange))
        self.assertEqual(len(fe), 2)
        self.assertTrue(isinstance(fe[0], MyRange))
        self.assertEqual(fe[0].start, 0)
        self.assertEqual(fe[0].stop, 2)
        self.assertTrue(isinstance(fe[1], MyRange))
        self.assertEqual(fe[1].start, 0)
        self.assertEqual(fe[1].stop, 2)

    def test_overlap(self):
        self.assertEqual(overlap(None, range(3, 7)), None)
        self.assertEqual(overlap(range(3, 7), None), None)
        self.assertEqual(overlap(range(-10, 10), range(3, 7, 2)), range(3, 7))
        self.assertEqual(overlap(range(-10, 10), range(10, 20, 3)), None)
        self.assertEqual(overlap(range(10, -10), range(10, -10)), None)
        self.assertEqual(overlap(range(-10, 10), range(0, 10)), range(0, 10))
        self.assertEqual(overlap(range(-10, 10), range(-20, 0, 2)), range(-10, 0))
        self.assertEqual(overlap(range(-10, 10), range(-20, -9)), range(-10, -9))
        r1 = MyRange(3, 7)
        r2 = range(-10, 5)
        o = overlap(r1, r2, construct=MyRange)
        self.assertTrue(isinstance(o, MyRange))
        self.assertEqual(o.start, 3)
        self.assertEqual(o.stop, 5)

    def test_filter_overlap(self):
        rs = (range(0, 10), range(10, 10), range(5, -5, 2), range(0, 10, 2))
        self.assertEqual(list(filter_overlap(rs, range(8, 20))), [range(0, 10), range(0, 10, 2)])
        self.assertEqual(list(filter_overlap(rs, range(8, 20), with_position=True)), [(0, range(0, 10)), (3, range(0, 10, 2))])
        self.assertEqual(list(filter_overlap(rs, range(8, 20), do_normalize=True)), [range(0, 10), range(0, 10)])
        self.assertEqual(list(filter_overlap(rs, range(8, 20), do_normalize=True, with_position=True)), [(0, range(0, 10)), (3, range(0, 10))])
        rs = [range(0, 10, 2), MyRange(10, 10), MyRange(5, -5), MyRange(0, 10)]
        self.assertEqual(list(filter_overlap(rs, range(8, 20), do_normalize=True)), [range(0, 10), range(0, 10)])
        ol = list(filter_overlap(rs, MyRange(8, 20), do_normalize=True, construct=MyRange))
        self.assertEqual(len(ol), 2)
        self.assertTrue(isinstance(ol[0], MyRange))
        self.assertEqual(ol[0].start, 0)
        self.assertEqual(ol[0].stop, 10)
        self.assertTrue(isinstance(ol[1], MyRange))
        self.assertEqual(ol[1].start, 0)
        self.assertEqual(ol[1].stop, 10)

    def test_match_count(self):
        self.assertEqual(match_count([], range(-1, 1)), 0)
        self.assertEqual(match_count([range(3, 7), range(-5, 0, 2), range(0, 1), range(1, 5), range(-1, 1)], range(-1, 1)), 3)

    def test_overlap_all(self):
        self.assertEqual(overlap_all([]), None)
        self.assertEqual(overlap_all([range(3, 7), range(-5, 0), range(0, 1), range(1, 5)]), None)
        self.assertEqual(overlap_all([range(2, 7), range(-5, 10, 5), range(0, 4), range(1, 5)]), range(2, 4))
        self.assertEqual(overlap_all([range(2, 7), range(-5, 10, 20), range(0, 4), None]), None)
        self.assertEqual(overlap_all([range(2, -7), range(-5, 10), range(0, 4)]), None)
        rs = [MyRange(2, 7), range(-5, 10), MyRange(0, 4), MyRange(1, 5)]
        o = overlap_all(rs, construct=MyRange)
        self.assertTrue(isinstance(o, MyRange))
        self.assertEqual(o.start, 2)
        self.assertEqual(o.stop, 4)

    def test_is_disjunct(self):
        rs = (range(0, 5), range(5, 10), range(10, 15, 3), range(20, 25))
        self.assertEqual(is_disjunct(rs, assume_ordered_increasingly=True), True)
        self.assertEqual(is_disjunct([], assume_ordered_increasingly=True), True)
        self.assertEqual(is_disjunct([], assume_ordered_increasingly=False), True)
        self.assertEqual(is_disjunct(rs), True)
        rs = (range(10, 15), range(20, 25), range(0, 5), range(5, 10))
        self.assertEqual(is_disjunct(rs), True)
        rs = (range(9, 15), range(20, 25), range(0, 5), range(5, 10))
        self.assertEqual(is_disjunct(rs), False)
        rs = (range(9, 15), range(20, 25), None, range(5, 10))
        self.assertEqual(is_disjunct(rs), False)
        rs = (range(11, 15), range(20, 25), None, range(5, 10))
        self.assertEqual(is_disjunct(rs), True)
        rs = (range(11, 15),)
        self.assertEqual(is_disjunct(rs), True)
        rs = (range(11, -5), range(6, 8))
        self.assertEqual(is_disjunct(rs), True)
        rs = (None,)
        self.assertEqual(is_disjunct(rs), True)

    def test_covering_all(self):
        rs = [range(3, 7), range(-5, 0), None, range(1, 5, 2)]
        self.assertEqual(covering_all(rs), range(-5, 7))
        self.assertEqual(covering_all([None, None]), None)
        self.assertEqual(covering_all([range(0, -10), None]), None)
        self.assertEqual(covering_all([range(1, 3, 3), range(2, 3)]), range(1, 3))
        self.assertEqual(covering_all([range(1, 3), range(2, 5, 7)]), range(1, 5))
        self.assertEqual(covering_all([range(1, 3), range(1, 3)]), range(1, 3))
        rs = [MyRange(3, 7), range(-5, 0), None, MyRange(1, 5)]
        o = covering_all(rs, construct=MyRange)
        self.assertTrue(isinstance(o, MyRange))
        self.assertEqual(o.start, -5)
        self.assertEqual(o.stop, 7)

    def test_contains(self):
        self.assertEqual(contains(range(0, 9), range(0, 9)), True)
        self.assertEqual(contains(range(3, 9), range(0, 9)), False)
        self.assertEqual(contains(range(0, 6), range(0, 9)), False)
        self.assertEqual(contains(range(3, 6), range(0, 9)), False)
        self.assertEqual(contains(None, range(6, 9)), False)
        self.assertEqual(contains(None, None), True)
        self.assertEqual(contains(range(1, 1), None), True)
        self.assertEqual(contains(range(1, 2), None), True)
        self.assertEqual(contains(range(1, 2), None), True)
        self.assertEqual(contains(range(1, 9), range(5, 9)), True)
        self.assertEqual(contains(range(1, 9), range(1, 5)), True)
        self.assertEqual(contains(range(1, 9), range(3, 5)), True)

    def test_filter_contained(self):
        rs = [range(0, 3), range(5, 8), None, range(10, 12, 3), range(10, 20)]
        rs2 = [range(5, 8), None, range(10, 12, 3)]
        rs2_w_pos = [(1, range(5, 8)), (2, None), (3, range(10, 12, 3))]
        self.assertEqual(list(filter_contained(rs, range(3, 15))), rs2)
        self.assertEqual(list(filter_contained(rs, range(5, 12))), rs2)
        self.assertEqual(list(filter_contained(rs, range(5, 11))), [range(5, 8), None])
        self.assertEqual(list(filter_contained(rs, range(3, 15), with_position=True)), rs2_w_pos)
        self.assertEqual(list(filter_contained(rs, range(5, 12), with_position=True)), rs2_w_pos)
        self.assertEqual(list(filter_contained(rs, range(5, 11), with_position=True)), [(1, range(5, 8)), (2, None)])
        self.assertEqual(list(filter_contained(rs, range(3, 15), do_normalize=True)), [range(5, 8), None, range(10, 12)])
        self.assertEqual(list(filter_contained(rs, range(3, 15), do_normalize=True, with_position=True)), [(1, range(5, 8)), (2, None), (3, range(10, 12))])
        rs = [MyRange(0, 3), MyRange(5, 8), None, range(10, 12, 3), MyRange(10, 20)]
        fc = list(filter_contained(rs, range(3, 15), do_normalize=True))
        self.assertEqual(fc, [range(5, 8), None, range(10, 12)])
        fc = list(filter_contained(rs, range(3, 15), do_normalize=True, construct=MyRange))
        self.assertTrue(isinstance(fc, list))
        self.assertEqual(len(fc), 3)
        self.assertTrue(isinstance(fc[0], MyRange))
        self.assertEqual(fc[0].start, 5)
        self.assertEqual(fc[0].stop, 8)
        self.assertEqual(fc[1], None)
        self.assertTrue(isinstance(fc[2], MyRange))
        self.assertEqual(fc[2].start, 10)
        self.assertEqual(fc[2].stop, 12)

    def test_is_covered_by(self):
        rs = [range(0, 3), range(5, 8), None, range(20, 30)]
        self.assertEqual(is_covered_by(rs, range(0, 30)), True)
        self.assertEqual(is_covered_by(rs, range(0, 20)), False)
        self.assertEqual(is_covered_by(rs, range(10, 30)), False)
        self.assertEqual(is_covered_by(rs, range(-5, 35)), True)

    def test_intermediate(self):
        self.assertEqual(intermediate(None, None), None)
        self.assertEqual(intermediate(range(0, 5), None), None)
        self.assertEqual(intermediate(None, range(0, 5)), None)
        self.assertEqual(intermediate(range(0, 5), range(5, 9)), None)
        self.assertEqual(intermediate(range(0, 5), range(10, 15)), range(5, 10))
        self.assertEqual(intermediate(range(10, 15), range(0, 5)), range(5, 10))
        self.assertEqual(intermediate(range(10, 15), range(0, 10)), None)
        self.assertEqual(intermediate(None, None, assume_ordered=True), None)
        self.assertEqual(intermediate(range(0, 5), None, assume_ordered=True), None)
        self.assertEqual(intermediate(None, range(0, 5), assume_ordered=True), None)
        self.assertEqual(intermediate(range(0, 5), range(5, 9), assume_ordered=True), None)
        self.assertEqual(intermediate(range(0, 5), range(10, 15), assume_ordered=True), range(5, 10))
        self.assertEqual(intermediate(range(10, 15), range(0, 5), assume_ordered=True), None)
        self.assertEqual(intermediate(range(10, 15), range(0, 10), assume_ordered=True), None)
        im = intermediate(MyRange(0, 5), range(10, 15), construct=MyRange)
        self.assertTrue(isinstance(im, MyRange))
        self.assertEqual(im.start, 5)
        self.assertEqual(im.stop, 10)

    def test_sort_by_start(self):
        rs1 = [range(1, 3), range(5, 7, 3), range(5, -5), None, range(-2, 10)]
        rs2 = [range(-2, 10), range(1, 3), range(5, 7, 3)]
        self.assertEqual(sort_by_start(rs1), rs2)

    def test_gaps(self):
        rs = [range(0, 1), range(1, 3), range(4, 6), range(6, 6), range(8, 10)]
        self.assertEqual(list(gaps(rs)), [range(3, 4), range(6, 8)])
        rs = [range(4, 6), range(6, 6), range(8, 10), range(0, 1), range(1, 3)]
        self.assertEqual(list(gaps(rs)), [range(3, 4), range(6, 8)])
        rs = [range(4, 6), range(4, 5), range(8, 10), range(0, 1), range(1, 3)]
        self.assertEqual(list(gaps(rs)), [range(3, 4), range(6, 8)])
        rs = [range(4, 6), range(6, 7), range(8, 10), range(0, 1), range(1, 3)]
        self.assertEqual(list(gaps(rs)), [range(3, 4), range(7, 8)])
        rs = [range(4, 6), range(6, 7), None, range(0, 1), range(1, 3)]
        self.assertEqual(list(gaps(rs)), [range(3, 4)])
        rs = [range(4, 6), range(6, 7), None, range(0, 1), range(1, 4)]
        self.assertEqual(list(gaps(rs)), [])
        rs = [range(8, 6), range(10, 17), None, range(0, 1), range(1, 5), range(1, 4), range(1, 8), range(1, 7)]
        self.assertEqual(list(gaps(rs)), [range(8, 10)])
        rs = [range(0, 1), range(2, 4), range(4, 6), range(6, 8), range(8, 10)]
        self.assertEqual(list(gaps(rs)), [range(1, 2)])
        rs = [MyRange(0, 1), range(2, 4), MyRange(4, 6), range(6, 8, 5), MyRange(8, 10)]
        g = list(gaps(rs, construct=MyRange))
        self.assertTrue(isinstance(g, list))
        self.assertEqual(len(g), 1)
        self.assertTrue(isinstance(g[0], MyRange))
        self.assertEqual(g[0].start, 1)
        self.assertEqual(g[0].stop, 2)

    def test_is_partition_of(self):
        rs = [range(0, 1), range(1, 4), range(4, 6), range(6, 8), range(8, 10)]
        self.assertEqual(is_partition_of(rs, assume_ordered=True), range(0, 10))
        rs = [range(0, 1), range(2, 4), range(4, 6), range(6, 8), range(8, 10)]
        self.assertEqual(is_partition_of(rs), None)
        rs = [range(8, 10), range(2, 4), range(0, 2), range(6, 6), None, range(4, 8)]
        self.assertEqual(is_partition_of(rs), range(0, 10))
        rs = [MyRange(8, 10), range(2, 4), MyRange(0, 2), range(6, 6), None, range(4, 8)]
        p = is_partition_of(rs, construct=MyRange)
        self.assertTrue(isinstance(p, MyRange))
        self.assertEqual(p.start, 0)
        self.assertEqual(p.stop, 10)

    def test_difference(self):
        self.assertEqual(difference(range(-5, -10), range(-8, -6)), (None, None))
        self.assertEqual(difference(range(-5, -10), range(-4, -6)), (None, None))
        self.assertEqual(difference(range(1, 2), range(4, 3)), (range(1, 2), None))
        self.assertEqual(difference(range(1, 9), range(2, 3)), (range(1, 2), range(3, 9)))
        self.assertEqual(difference(range(1, 9), range(1, 3)), (None, range(3, 9)))
        self.assertEqual(difference(range(1, 9), range(3, 9)), (range(1, 3), None))
        self.assertEqual(difference(range(1, 9), range(-3, 9)), (None, None))
        self.assertEqual(difference(range(1, 9), range(-3, 20)), (None, None))
        self.assertEqual(difference(range(1, 9), range(1, 9)), (None, None))
        self.assertEqual(difference(range(1, 9), range(-3, 5)), (None, range(5, 9)))
        self.assertEqual(difference(range(1, 9), range(5, 15)), (range(1, 5), None))
        r1, r2 = difference(MyRange(1, 9), range(3, 9, 3), construct=MyRange)
        self.assertTrue(isinstance(r1, MyRange))
        self.assertEqual(r1.start, 1)
        self.assertEqual(r1.stop, 3)
        self.assertEqual(r2, None)

    def test_normalize_multi(self):
        rs = []
        self.assertEqual(list(normalize_multi(rs)), [])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [])
        rs = [range(0, 1)]
        self.assertEqual(list(normalize_multi(rs)), [range(0, 1)])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [range(0, 1)])
        rs = [range(0, 2), range(4, 5), range(5, 7, 3)]
        self.assertEqual(list(normalize_multi(rs)), [range(0, 2), range(4, 7)])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [range(0, 2), range(4, 7)])
        rs = [range(0, 2), range(3, 8), range(4, 5), range(5, 7)]
        self.assertEqual(list(normalize_multi(rs)), [range(0, 2), range(3, 8)])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [range(0, 2), range(3, 8)])
        rs = [range(0, 2), range(0, 5), range(5, 7), range(8, 8)]
        self.assertEqual(list(normalize_multi(rs)), [range(0, 7)])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [range(0, 7)])
        rs = [None, range(0, 5), range(5, 7), range(8, 20)]
        self.assertEqual(list(normalize_multi(rs)), [range(0, 7), range(8, 20)])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [range(0, 7), range(8, 20)])
        rs = [None, range(0, 5), range(6, 8), range(8, 20)]
        self.assertEqual(list(normalize_multi(rs)), [range(0, 5), range(6, 20)])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [range(0, 5), range(6, 20)])
        rs = [None, range(0, 5), range(6, 8), range(20, 20)]
        self.assertEqual(list(normalize_multi(rs)), [range(0, 5), range(6, 8)])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [range(0, 5), range(6, 8)])
        rs = [None, range(0, 5), range(6, 8), range(6, 9)]
        self.assertEqual(list(normalize_multi(rs)), [range(0, 5), range(6, 9)])
        self.assertEqual(list(normalize_multi(rs, assume_ordered_increasingly=True)), [range(0, 5), range(6, 9)])
        rs = [None, MyRange(0, 5), range(6, 8), MyRange(6, 9)]
        n = list(normalize_multi(rs, construct=MyRange))
        self.assertEqual(len(n), 2)
        self.assertTrue(isinstance(n[0], MyRange))
        self.assertEqual(n[0].start, 0)
        self.assertEqual(n[0].stop, 5)
        self.assertTrue(isinstance(n[1], MyRange))
        self.assertEqual(n[1].start, 6)
        self.assertEqual(n[1].stop, 9)

    def test_difference_one_multi(self):
        r = range(0, 20, 3)
        mr1 = [range(2, 4), range(6, 8)]
        self.assertEqual(list(difference_one_multi(r, mr1)), [range(0, 2), range(4, 6), range(8, 20)])
        mr2 = [range(-2, 1), range(2, 4), range(6, 8), range(15, 25)]
        self.assertEqual(list(difference_one_multi(r, mr2)), [range(1, 2), range(4, 6), range(8, 15)])
        mr3 = [range(-2, 0), range(2, 4), range(6, 8), range(20, 25)]
        self.assertEqual(list(difference_one_multi(r, mr3)), [range(0, 2), range(4, 6), range(8, 20)])
        r = MyRange(0, 20)
        mr = [MyRange(-2, 0), range(2, 4), MyRange(6, 8), range(20, 25)]
        d = list(difference_one_multi(r, mr, construct=MyRange))
        self.assertEqual(len(d), 3)
        self.assertTrue(isinstance(d[0], MyRange))
        self.assertEqual(d[0].start, 0)
        self.assertEqual(d[0].stop, 2)
        self.assertTrue(isinstance(d[1], MyRange))
        self.assertEqual(d[1].start, 4)
        self.assertEqual(d[1].stop, 6)
        self.assertTrue(isinstance(d[2], MyRange))
        self.assertEqual(d[2].start, 8)
        self.assertEqual(d[2].stop, 20)


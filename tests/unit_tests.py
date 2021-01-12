#!/usr/bin/env python3
import unittest

from calc import OPERATORS, calculate
from db import connect_db


class TestCalc(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(calculate("3,+,4"), (7, 0, 'OK'))

    def test_sub(self):
        self.assertEqual(calculate("3,-,4"), (-1, 0, 'OK'))

    def test_mul(self):
        self.assertEqual(calculate("2,*,3"), (6, 0, 'OK'))

    def test_pow(self):
        self.assertEqual(calculate("2,**,3"), (8, 0, 'OK'))

    def test_div(self):
        self.assertEqual(calculate("4,/,2"), (2, 0, 'OK'))

    def test_dbcon(self):
        db_con = connect_db()
        db_cur =  db_con.cursor()
        db_info = db_cur.execute('PRAGMA table_info(results)').fetchall()
        for i in range(0, len(db_info)):
            db_info[i] = tuple(db_info[i])
        self.assertEqual(sorted(db_info),
            [(0, 'id', 'blob', 0, None, 0),
            (1, 'operation', 'text', 0, None, 0),
            (2, 'result', 'integer', 0, None, 0)])

if __name__ == '__main__':
    unittest.main()

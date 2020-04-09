import unittest
from typing import Dict, DefaultDict
from collections import defaultdict
from HW08_Jim_Rowland import file_reader
import os
from prettytable import PrettyTable
from HW09_Minakshi_Tiwari_Testcode import Student, Instructor, Repository


class TestRepository(unittest.TestCase):
    """Test for pretty table  inside Repository class"""

    def test_student_pretty_table(self):
        """Test cases for student pretty table"""
        self.repository = Repository(':\\Users\\Barun Pandey\\Documents\\Stevens\\Special Topics in Software Engineering\\Homeworks\\Assignment no.9')
        calculated_table = {cwid: students.student_pretty_table() for cwid, students in self.repository._students.items()}
        expected = {'10103': ['10103', 'Baldwin, C', ['SSW 564', 'SSW 567']], '10115': ['10115', 'Wyatt, X', ['SSW 564','SSW 567']]}
        self.assertEqual(expected, calculated_table)

    def test_instructor_pretty_table(self):
        """Test cases for instructor pretty table"""
        self.repository = Repository(':\\Users\\Barun Pandey\\Documents\\Stevens\\Special Topics in Software Engineering\\Homeworks\\Assignment no.9')
        calculated = {cwid: instructors.instructor_pretty_table() for cwid, instructors in self.repository._instructors.items()}
        expected_table = {'98765': ['98765', 'Einstein, A', 'SFEN', 'SSW 567', '2' ], '98764': ['98764', 'Feynman, R', 'SFEN', 'SSW 564', '2']}
        self.assertEqual(expected_table, calculated)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)

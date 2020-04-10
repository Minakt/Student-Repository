
import os
import unittest
from typing import Iterator, Tuple, Dict, List
from HW10_Minakshi_Tiwari import Student, Instructor, University, Major
from HW08_Jim_Rowland import file_reader


class TestUniversity(unittest.TestCase):
    """Test for pretty table  inside University class"""

    def test_check(self):
        self.directory = "/Users/minakshitiwari/Documents/MS Courses/810-Special Topics in Software Engineering./week ten"
        self.uni = University(self.directory, False)


    def test_major(self):
        """ Testing majors table"""
        expected_result = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']],
                   ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]]

        computed_result = [majors.major_prettytable() for majors in self.uni._majors.values()]
        self.assertEqual(expected_result, computed_result)

    def test_Student(self):
        """ Testing student table """
        expected_result = [
        [['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, {},
          3.44],
         ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, {},
          3.81],
         ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], {'SSW 564', 'SSW 540'}, {'SSW 555', 'SSW 567'},
          3.88],
         ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'},
          {'SSW 567', 'SSW 687', 'SSW 564'}, 3.58],
         ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], {'SSW 555', 'SSW 564', 'SSW 540', 'SSW 567'}, {'SSW 689'},
          4.0],
         ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, {}, 3.0],
         ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 612', 'SYS 671'},
          {'SYS 800', 'SYS 750', 'SYS 611'}, 3.92],
         ['11658', 'Kelly, P', 'SYEN', [], {'SYS 612', 'SYS 671', 'SYS 800'}, set(), 0.0],
         ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], {'SYS 612', 'SYS 671', 'SYS 800'},
          {'SYS 645', 'SYS 611'}, 3.0],
         ['11788', 'Fuller, E', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, {}, 4.0]]]
        computed_result = [[student.info() for cwid, student in self.uni._students.items()]]
        self.assertEqual(expected_result, computed_result)

    def test_Instructor(self):
        """Testcase for instructor"""
        expected_result = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
               ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
               ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
               ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
               ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
               ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
               ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
               ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
               ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
               ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
               ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
               ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}
        computed_result = {tuple(detail) for instructor in self.uni._instructors.values() for detail in
               instructor.instructor_info()}
        self.assertEqual(expected_result, computed_result)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)

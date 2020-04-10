import os
from collections import defaultdict
from prettytable import PrettyTable
from typing import Dict, Set, List, Iterator, Tuple, DefaultDict
from HW08_Jim_Rowland import file_reader


class University:
    """ Store the records of students and instructors """

    def __init__(self, dir: str, hd=True):
        """ Initialize directory and dictionary for students and instructor"""
        self._dir: str = dir
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self._majors: Dict[str, Major] = dict()

        try:
            self._get_majors(os.path.join(dir, "majors.txt"))
            self._get_students(os.path.join(dir, "students.txt"))
            self._get_instructors(os.path.join(dir, "instructors.txt"))
            self._get_grades(os.path.join(dir, "grades.txt"))

        except (FileNotFoundError, ValueError) as v:
            print(v)
        else:
            if hd:
                print("Student summary table")
                self.student_table()

                print("Instructor summary table")
                self.instructor_table()

                print("Majors Table")
                self.majors_table()

    def _get_majors(self, path):
        """Major details are read using file reading gen and added to dictionary"""
        try:
            maj_info: Iterator[Tuple[str]] = file_reader(
                path, 3, sep='\t', header=True)
            for major, flag, course in maj_info:
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].add_remain_elec(course, flag)
        except ValueError as v:
            print(v)

    def _get_students(self, path):
        """ Student detail are read using file reading gen and added to dictionary """
        try:
            stu_info: Iterator[Tuple[str]] = file_reader(
                path, 3, sep=';', header=True)
            for cwid, name, major in stu_info:
                if major not in self._majors:
                    print(
                        f"Student {cwid} '{name}' has unknown major '{major}'")
                else:
                    self._students[cwid] = Student(
                        cwid, name, self._majors[major])
        except ValueError as v:
            print(v)

    def _get_instructors(self, path: str):
        """ Get the instructor details from the file and store it in the dictionary"""
        try:
            ins_info: Iterator[Tuple[str]] = file_reader(
                path, 3, sep='|', header=True)
            for cwid, name, dept in ins_info:
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as v:
            print(v)

    def _get_grades(self, path: str):
        """ Get the student grades details from the file and store it in the dictionary"""
        try:
            grade_info = file_reader(path, 4, sep='|', header=True)
            for stu_cwid, course, grade, inst_cwid in grade_info:
                if stu_cwid in self._students:
                    self._students[stu_cwid].add_course(course, grade)
                else:
                    print(f"Grade for unknown student {stu_cwid}")

                if inst_cwid in self._instructors:
                    self._instructors[inst_cwid].add_student(course)
                else:
                    print(f"Grade for unknown instructor {inst_cwid}")
        except ValueError as v:
            print(v)

    def student_table(self):
        """ Pretty table for the students """
        Table: PrettyTable = PrettyTable(
            field_names=Student.prettytable_header)
        a = list()
        for student in self._students.values():
            Table.add_row(student.ptable_row())
            a.append(student.ptable_row())

        print(Table)

    def instructor_table(self):
        """ Pretty table for the instructors """
        Table: PrettyTable = PrettyTable(
            field_names=Instructor.prettytable_header2)

        for instructor in self._instructors.values():
            for row in instructor.ptable_row():
                Table.add_row(row)
        print(Table)

    def majors_table(self):
        """ Pretty table for majors """
        Table: PrettyTable = PrettyTable(field_names=Major.titles)

        for major in self._majors.values():
            Table.add_row(major.ptable_row())
        print(Table)


class Major:
    """ Major Class """
    titles = ['Major', 'Required Courses', 'Electives']
    grades_given = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def __init__(self, dept):
        self._dept: str = dept
        self._required: Set = set()
        self._electives: Set = set()

    def add_remain_elec(self, course, req):
        if req == 'R':
            self._required.add(course)
        elif req == 'E':
            self._electives.add(course)
        else:
            raise ValueError("Course not found")

    def remaining_courses(self, completed):
        """Adding remaining required  courses as well as remaining electives"""
        completed = {course for course, grade in completed.items()
                     if grade in Major.grades_given}
        if self._required.difference(completed) == None:
            rem_required = None
        else:
            rem_required = self._required - completed
        if self._electives.difference(completed) == None:
            rem_electives = None
        else:
            rem_electives = self._electives - completed

        return self._dept, completed, rem_required, rem_electives

    def ptable_row(self):
        """ Returning a majors prettytable """
        return [self._dept, sorted(self._required), sorted(self._electives)]


class Student:
    """ Student class """
    prettytable_header = ["CWID", "Name", "Major", "Completed Courses",
                          "Remaining Required", "Remaining Electives", "GPA"]

    def __init__(self, cwid, name, major):
        """ Initialize student table details """
        self._cwid: int = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def add_course(self, course, grade):
        """ Adding course with grade """
        self._courses[course] = grade

    def gpa(self):
        """calculate the GPA using dictionary"""
        grades: Dict[str, float] = {"A": 4.00, "A-": 3.75, "B+": 3.25, "B": 3.00, "B-": 2.75, "C+": 2.25, "C": 2.00, "C-": 0.00,
                                    "D+": 0.00, "D": 0.00, "D-": 0.00, "F": 0.00}
        try:
            total: float = sum(
                [grades[grade] for grade in self._courses.values()]) / len(self._courses.values())
            return round(total, 2)
        except ZeroDivisionError as z:
            print(z)

    def ptable_row(self):
        """ Returning a student prettytable """
        major, passed, rem_required, rem_electives = self._major.remaining_courses(
            self._courses)
        return [self._cwid, self._name, major, sorted(passed), sorted(rem_required), sorted(rem_electives), self.gpa()]


class Instructor:
    """ Instructor class """
    prettytable_header2 = ["CWID", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid: int, name: str, dept: str):
        """ Initialize instructor table details """
        self._cwid: int = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses_i: DefaultDict[str, int] = defaultdict(int)

    def add_student(self, course):
        """ Counting the number of students took the course with this instructor """
        self._courses_i[course] += 1

    def ptable_row(self):
        """ Yield the rows for instructor prettytable """
        for course, count in self._courses_i.items():
            yield [self._cwid, self._name, self._dept, course, count]


def main():
    """ Pass the directory to Repository class """
    University('/Users/minakshitiwari/Documents/MS Courses/810-Special Topics in Software Engineering./week ten')


if __name__ == '__main__':
    """ Run main function on start """
    main()


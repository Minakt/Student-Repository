from typing import Dict, DefaultDict, Tuple, Iterator, List, Any
from collections import defaultdict
import os
import sqlite3
from prettytable import PrettyTable
from HW08_Jim_Rowland import file_reader


class University:

    """Store all students, instructors for a university and print a pretty table"""

    def __init__(self, dir: str, header, db_path: str):
        """Store all students, instructors,
         read student.txt, grades.txt, instructors.txt
        print prettytables"""
        self._dir: str = dir
        # _students(cwid) = Student()
        self.db_path = db_path
        self._students: Dict[str, Student] = dict()
        # _instructors(cwid) = Instructor()
        self._instructors: Dict[str, Instructor] = dict()
        self._majors: Dict[str, Major] = dict()
        # read the students file and create instances for the class student
        # read the instructors file and create instances for the class instructor
        # read the grades file and process each grade
        try:
            self.student_summary_grade(os.path.join(dir, self.db_path))
            self._read_majors(os.path.join(dir, "majors.txt"))
            self._read_students(os.path.join(dir, "students.txt"))
            self._read_instructors(os.path.join(dir, "instructors.txt"))
            self._read_grades(os.path.join(dir, "grades.txt"))

        except FileNotFoundError:
            print(f"{dir} cannot be opened")
        else:
            if header:
                print("Student summary")
                self.student_pretty_table()
                print("Instructor summary")
                self.instructor_pretty_table()
                print("Majors summary")
                self.majors_table()
                print("student grade table")
                self.student_grade_table()

    def _read_majors(self, path):
        """Major details are read using file reading gen and added to dictionary"""
        try:
            for major, flag, course in file_reader(path, 3, sep='\t', header=True):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].store_electives(course, flag)
        except ValueError as v:
            print(v)

    def _read_students(self, path: str):
        """ Read each line"""
        try:
            data1: Iterator[Tuple[str]] = file_reader(
                path, 3, sep='\t', header=True)
            for cwid, name, major in data1:
                if major not in self._majors:
                    print(
                        f"Student {cwid} '{name}' informations is undefined '{major}'")
                else:
                    self._students[cwid] = Student(
                        cwid, name, self._majors[major])
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_instructors(self, path: str):
        """ Read each line"""
        try:
            data2: Iterator[Tuple[str]] = file_reader(
                path, 3, sep='\t', header=True)
            for cwid, name, dept in data2:
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as i:
            print(i)

    def _read_grades(self, path: str):
        """Read the students cwid, course, grades, instructors_cwid"""
        # tell the student about the course and the grade
        # Look up the student associated with student_cwid, reach, inside, and update the dictionary inside student

        try:
            data3 = file_reader(path, 4, sep='\t', header=True)
            for student_cwid, course, grade, instructor_cwid in data3:
                if student_cwid in self._students:
                    self._students[student_cwid].store_course_grade(
                        course, grade)
                else:
                    print(
                        f"Grade for the student {student_cwid} not reflectd in student's file in {course} is {grade}")

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].store_course_student(
                        course)
                else:
                    print(
                        f"Unknown instructor {instructor_cwid} not reflected in the instructor's file")

        except(FileNotFoundError, ValueError) as j:
            print(j)

    def student_summary_grade(self, db_path):
        db: sqlite3.Connection = sqlite3.connect(self.db_path)
        queries = """SELECT S.Name,S.CWID,G.Course,G.Grade,I.Name
                    FROM students AS S JOIN grades AS G ON S.CWID = G.StudentCWID
                    JOIN instructors AS I ON G.InstructorCWID=I.CWID
                    order by s.Name"""
        for NAME, CWID, COURSE, GRADE, INSTNAME in db.execute(queries):
            yield NAME, CWID, COURSE, GRADE, INSTNAME

    def student_pretty_table(self) -> None:
        """Print a pretty table with student information"""
        pt: PrettyTable = PrettyTable(field_names=Student.PT_FIELD_NAMES1)
        for student in self._students.values():
            pt.add_row(student.info())
            # add a row to the pretty table
        print(pt)

    def instructor_pretty_table(self):
        """Print a pretty table with instructor information"""
        pt: PrettyTable = PrettyTable(field_names=Instructor.PT_FIELD_NAMES2)
        for instructor in self._instructors.values():
            for row in instructor.instructor_info():
                pt.add_row(row)
        print(pt)

    def majors_table(self):
        pt = PrettyTable(field_names=Major.PT_FIELD_NAMES3)

        for major in self._majors.values():
            pt.add_row(major.majors_pretty_table())
        print(pt)

    def student_grade_table(self) -> PrettyTable:
        """ Summary of student_grade table """
        pt: PrettyTable = PrettyTable(
            field_names=['Name', 'cwid', 'course', 'grade', 'Instructor'])
        for studs in self.student_summary_grade(self.db_path):
            pt.add_row(studs)
        print(pt)


class Major:
    PT_FIELD_NAMES3 = ['Major', 'Required Courses', 'Electives Courses']
    grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def __init__(self, dept):
        self._dept: str = dept
        self._required_courses = set()
        self._electives_courses = set()

    def store_electives(self, course, required):
        if required == 'R':
            self._required_courses.add(course)
        elif required == 'E':
            self._electives_courses.add(course)
        else:
            print('unknown course')

    def remaining_courses(self, completed_Courses: str):
        completed = {course for course, grade in completed_Courses.items()
                     if grade in Major.grades}
        if self._required_courses.difference(completed) == None:
            rem_required = None
        else:
            rem_required = self._required_courses - completed
        if self._electives_courses.difference(completed) == None:
            rem_electives = None
        else:
            rem_electives = self._electives_courses - completed

        return self._dept, completed, rem_required, rem_electives

    def majors_pretty_table(self):
        """ Returning a majors prettytable """
        return [self._dept, sorted(self._required_courses), sorted(self._electives_courses)]


class Student:
    """Store everything about a single student"""
    PT_FIELD_NAMES1: Tuple[str, str, str, str, str, str, str] = ['CWID', 'Name', 'Major', 'Electives Courses',
                                                                 'Completed Courses', 'Remaining Required', 'GPA']

    def __init__(self, cwid, name, major) -> None:
        """This is a constructor. Professor did not use any self in the argument of the class above"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()  # courses(course_name) = grade

    def store_course_grade(self, course, grade):
        self._courses[course] = grade

    def gpa(self):
        grades: Dict[str, float] = {"A": 4.00, "A-": 3.75, "B+": 3.25, "B": 3.00, "B-": 2.75, "C+": 2.25, "C": 2.00, "C-": 0.00,
                                    "D+": 0.00, "D": 0.00, "D-": 0.00, "F": 0.00}
        try:
            total: float = sum(
                [grades[grade] for grade in self._courses.values()]) / len(self._courses.values())
            return round(total, 2)
        except:
            print('error found')

    def info(self):
        """return a list of information about me/self needed for the pretty table"""
        major, passed, remaining_courses, electives_courses = self._major.remaining_courses(
            self._courses)
        return [self._cwid, self._name, major, sorted(passed), sorted(remaining_courses), sorted(electives_courses), self.gpa()]


class Instructor:
    """Store everything about a single student"""
    PT_FIELD_NAMES2 = ['CWID', 'Name', 'Dept', 'Courses', 'Students']

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        """This is a constructor. Professor did not use any self in the argument of the class above"""
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)
        # courses(course_name) = #number of students who have taken that class

    """Finish line"""

    def store_course_student(self, course: str):
        """ Note that instructor taught one more student in course"""
        self._courses[course] += 1

    def instructor_info(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """return a list of information about self needed for the pretty table"""
        for course, student_count in self._courses.items():
            yield self._cwid, self._name, self._dept, course, student_count


def main():
    """Define two repositories- one for Stevens and one for NYU"""
    University('/Users/minakshitiwari/Documents/MS Courses/810-Special Topics in Software Engineering./Week eleven', True,
               '/Users/minakshitiwari/Documents/MS Courses/810-Special Topics in Software Engineering./Week eleven/810_minakshi.db')


if __name__ == '__main__':
    """ Run main function on start """
    main()

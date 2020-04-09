from typing import Dict, DefaultDict, List, Iterator, Tuple, Any
from collections import defaultdict
from HW08_Jim_Rowland import file_reader
import os
from prettytable import PrettyTable


class Student:
    """Store data of a single student"""
    PT_FIELD_NAMES1: Tuple[str, str, str] = [
        'CWID', 'Name', 'Completed Courses']

    def __init___(self, cwid: str, name: str, major: str):
        """Constructor with student id, name and major as arguments"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()  # courses(course_name) = grade

    def store_course_grade(self, course: str, grade: str) -> None:
        """The student took course and earned grade"""
        self._courses[course] = grade

    def info(self) -> Tuple[str, str, List[str]]:
        """return a list of information about self needed for the pretty table"""

        return self._cwid, self._name, sorted(self._courses.keys())


class Instructor:
    PT_FIELD_NAMES2: List[str] = ['CWID', 'Name', 'dept', 'course', 'students']

    def __init___(self, cwid: str, name: str, dept: str) -> None:
        """This is a constructor. Professor did not use any self in the argument of the class above"""
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)
        # courses(course_name) = #number of students who have taken that class

    def store_course_student(self, course: str) -> None:
        """ Instructor taught one more student in course"""
        self._courses[course] += 1

    def instructor_info(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """return a list of information about self needed for the pretty table"""
        for course, student_count in self._courses.items():
            yield self._cwid, self._name, self._dept, course, student_count


class Repository:
    """Store all students, instructors for a university and print a pretty table"""

    def __init__(self, dir: str, ptable: bool = True) -> None:
        """Store all students, instructors,
         read student.txt, grades.txt, instructors.txt
        print prettytables"""
        self._dir: str = dir
        # _students(cwid) = Student()
        self._students: Dict[str, Student] = dict()
        # _instructors(cwid) = Instructor()
        self._instructors: Dict[str, Instructor] = dict()

        # read the students file and create instances for the class student
        # read the instructors file and create instances for the class instructor
        # read the grades file and process each grade
        try:
            self._read_students(os.path.join(dir, "students.txt"))
            self._read_instructors(os.path.join(dir, "instructors.txt"))
            self._read_grades(os.path.join(dir, "grades.txt"))
        except FileNotFoundError:
            print('f')
        if ptable:
            print("Student summary")
            self.student_pretty_table()
            print("Instructor summary")
            self.instructor_pretty_table()

    def _read_students(self, path: str) -> None:
        """ Read each line in the file"""
        try:
            for cwid, name, major in file_reader(path, 3, sep='\t', header=False):
                self._students[cwid] = Student(cwid, name, major)
                # do something
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_instructors(self, path: str) -> None:
        """ Read each line in the file"""
        try:
            for cwid, name, dept in file_reader(path, 3, sep='\t', header=False):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except(FileNotFoundError, ValueError) as i:
            print(i)

    def _read_grades(self, path: str) -> None:
        """Read the students_cwid, course, grades and  instructors_cwid"""
        # tell the student about the course and the grade
        # Look up the student associated with student_cwid, reach, inside, and update the dictionary inside student

        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(path, 4, sep='\t', header=False):
                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade)
                else:
                    print(
                        f"Grade for the student {student_cwid} not reflectd in student's file in {course} is {grade}")

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_student(course)
                else:
                    print(
                        f"Unknown instructor {instructor_cwid} not reflected in the instructor's file")

        except(FileNotFoundError, ValueError) as j:
            print(j)

    def student_pretty_table(self) -> None:
        """Print a pretty table with student information"""
        pt: PrettyTable = PrettyTable(field_names=Student.PT_FIELD_NAMES1)
        for student in self._students.values():
            pt.add_row(student.info())
            # add a row to the pretty table
        print(pt)

    def instructor_pretty_table(self) -> None:
        """Print a pretty table with instructor information"""
        pt: PrettyTable = PrettyTable(field_names=Instructor.PT_FIELD_NAMES2)
        for instructor in self._instructors.values():
            for row in instructor.pt_rows():
                pt.add_row(row)
        print(pt)


def main():
    """Define a repositories for data files"""
    directory: str = "/Users/minakshitiwari/Documents/MS Courses/810-Special Topics in Software Engineering./Nine assignment"


if __name__ == '__main__':
    """ Run main function on start """
    main()

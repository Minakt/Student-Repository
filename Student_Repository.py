from flask import Flask, render_template
import sqlite3
from typing import Dict

db_path: str = '/Users/minakshitiwari/Documents/MS Courses/810-Special Topics in Software Engineering./Week eleven/810_minakshi.db'

app: Flask = Flask(__name__)


@app.route("/completed")
def completed_summary() -> str:
    db: sqlite3.Connection = sqlite3.connect(db_path)
    query = """SELECT S.Name,S.cwid,G.Course,G.grade,I.Name
                    FROM students AS S JOIN grades AS G ON S.CWID = G.StudentCWID
                    JOIN Instructors AS I ON G.InstructorCWID=I.CWID
                    order by s.Name"""

    data: Dict[str, str] =\
        [{'name': name, 'cwid': cwid, 'course': course, 'grade': grade, 'Instructor': Instructor}
            for name, cwid, course, grade, Instructor in db.execute(query)]
    db.close()

    return render_template('student_course.html',
                           title='Repository',
                           table_title='table',
                           students=data)


if __name__ == '__main__':
    app.run(debug=True)

"""
    implement a general purpose ascii file reader that opens a file and yields
    the contents of that file line by line on calls to next()
"""

from datetime import datetime, timedelta
import unittest
import os
from prettytable import PrettyTable
from collections import defaultdict
from typing import IO, List, Tuple, Dict, DefaultDict, Iterator

def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ return a tuple with
        - the date three days after Feb 27, 2020
        - the date three days after Feb 27, 2019
        - How many days passed between Feb 1, 2019 and Sept 30, 2019
    """
    dt_str: str = "2/27/2020"
    dt_20200227: datetime = datetime.strptime(dt_str, "%m/%d/%Y")  # or just do datetime(2020, 2, 27)
    delta1: timedelta = timedelta(days=3)
    dt1: datetime = dt_20200227 + delta1

    dt_20190227: datetime = datetime(2019, 2, 27)
    delta2: timedelta = timedelta(days=3)
    dt2: datetime = dt_20190227 + delta2

    dt_20190930: datetime = datetime(2019, 9, 30)
    dt_20190201: datetime = datetime(2019, 2, 1)
    delta3:timedelta = dt_20190930 - dt_20190201

    return dt1, dt2, delta3.days

def file_reader(path: str, num_fields: int, sep: str=',', header: bool=False) -> Iterator[List[str]]:
    """ Attempt to open 'path' for reading.  Read the file line by line and 
        return the fields as a tuple on each call to next().
        - path specifies the file path
        - num_fields is the number of fields expected to be read from each line in the file
        - sep is the field separator
        - header specifies if the first row in the file is a header row.  

        If the first row is a header then check the header for the proper number of fields but
        don't yield the header row

        Exceptions:
        - raise FileNotFoundError if the file can't be opened
        - raise ValueError if the number of fields read doesn't match num_fields  
    """
    try:
        fp: IO = open(path, "r", encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Can't open '{path}' for reading")
    else:
        with fp:
            for n, line in enumerate(fp, 1):
                fields: List[str] = line.rstrip('\n').split(sep)
                if len(fields) != num_fields:
                    raise ValueError(f"'{path}' line: {n}: read {len(fields)} fields but expected {num_fields}")
                elif n > 1 or header is False:  # if past the first line or no header, then yield the fields
                    yield fields


class FileAnalyzer:
    """
        Given a directory, search that directory for Python files (those ending with .py).
        Open each file and calculate a summary including:
        - the file name
        - the number of classes defined in the file
        - the number of Python methods/functions (lines that begin with 'def ')
        - the total number of lines in the file
        - the total number of characters in the file
    """
    def __init__(self, directory: str) -> None:
        """ summarize directory with number of classes, functions, lines, and chars
            in each .py file in a directory
        """
        self.directory: str = directory 

        """
        files_summary[file_name] = {'class': # number of classes in the file,
                                    'function': # number of functions in the file,
                                    'line': # number of lines in the file,
                                    'char': # number of characters in the file,}
        """
        self.files_summary: Dict[str, Dict[str, int]] = self.analyze_files() 

    def analyze_files(self) -> Dict[str, Dict[str, int]]:
        """ Summarize the directory at self.directory and return a dict with the number of
            classes, functions, lines, and characters
            Raise FileNotFound if the directory can't be opened
            Raise FileNotFound if any file in the directory can't be opened
        """
        result: Dict[str, Dict[str, int]] = dict()
        try:
            files: List[str] = os.listdir(self.directory)
        except FileNotFoundError:
            raise FileNotFoundError(f"Directory {self.directory} was not found")
        else:
            for f in files:
                if f.lower().endswith('.py'):
                    path: str = os.path.join(self.directory, f)
                    try:
                        result[path] = self.process_file(path)  # get the counts from the file and populate self.file_summary
                    except FileNotFoundError as fnfe:
                        raise fnfe

        return result

    def process_file(self, path: str) -> Dict[str, int]:
        """ summarize the contents of one Python file
            Return a tuple with classes, functions, lines, chars found in this file
            Raise FileNotFoundError if unable to open the file
        """
        try:
            fp: IO = open(path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open '{path}'")
        else:
            with fp:
                counts: DefaultDict[str, int] = defaultdict(int)
                for line in fp:
                    counts['char'] += len(line)  # calculate total chars before stripping
                    counts['line'] += 1  # found one more line
                    line = line.strip()  # strip newline and any leading or trailing whitespace
                    if line.startswith('class '):
                        counts['class'] += 1
                    elif line.startswith('def '):
                        counts['function'] += 1

                return counts  # return the counts to be added to file_summary

    def pretty_print(self) -> PrettyTable:
        """ print a prettytable with the results for the directory """
        pt: PrettyTable = PrettyTable(field_names=['File Name', 'Classes', 'Functions', 'Lines', 'Characters'])
        for file, counts in self.files_summary.items():
            pt.add_row([file, counts['class'], counts['function'], counts['line'], counts['char'],])

        return pt


#### include below here for grading

def file_reader_demo(path, fields, sep, header):
    try:
        for fields in file_reader(path, fields, sep=sep, header=header):
            print(fields)
    except FileNotFoundError as fnfe:
        print("Detected FileNotFound:", fnfe)
    except ValueError as ve:
        print("Detected Wrong # of Fields", ve)
            
def main():
    path = "/Users/jrr/Documents/Stevens/810/Assignments/HW08_FileReader/test3.txt"
    print("should show 2 rows with 5 fields")
    file_reader_demo(path, 5, sep='#', header=True)

    path = "/Users/jrr/Documents/Stevens/810/Assignments/HW08_FileReader/test5.txt"
    print("\nshould raise exception for wrong fields: line: 1: read 4 fields but expected 5")
    file_reader_demo(path, 5, sep='#', header=True)

    path = "/Users/jrr/Documents/Stevens/810/Assignments/HW08_FileReader/NOTFOUND.txt"
    print("\nshould raise exception for bad file")
    file_reader_demo(path, 5, '#', True)


    d = '/Users/jrr/Documents/Stevens/810/Assignments/HW08_Test/'
    try:
        fa = FileAnalyzer(d)
    except FileNotFoundError as e:
        print("FileAnalyzer FNFE:",e)
    else:
        print("FileAnalyze PrettyTable")
        print(fa.pretty_print())
            


if __name__ == '__main__':
    main()

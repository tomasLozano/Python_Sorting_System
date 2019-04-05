
import unittest
import main_project
import pandas

"""
By Tomas Lozano
CST8333 Programming Language Research Project

Test unit
"""

class test_Main_Project(unittest.TestCase):
    print("\nBy Tomas Lozano - 040869662")
    print("CST8333 Programming Language Research Project")
    print("Last modified: 2018-12-01\n")


    def test_count_row(self):
        self.dr = pandas.read_csv('32100054.csv')
        self.assertTrue(len(self.dr) == 30559)
    
    def test_isInherited(self):
        self.assertTrue(issubclass(main_project.myInfo, main_project.info))

if __name__ == '__main__':
        unittest.main()

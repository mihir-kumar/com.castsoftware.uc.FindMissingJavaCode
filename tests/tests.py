'''
Created on 5 janv. 2015

@author: MRO
'''
import unittest
from cast.application.test import run




class Test(unittest.TestCase):


    def test_basic(self):

        run(kb_name='findsource_local', application_name='FindMissingSource') 


if __name__ == "__main__":

    unittest.main()

    
    
'''
Integration tests for bobskater obfuscation
'''
import unittest
import logging
import re

from bobskater.obfuscate import obfuscateString

logging.basicConfig(format='%(name)s|%(levelname)s: %(message)s', \
    datefmt='%I:%M:%S %p', \
    level=logging.DEBUG)

class TestBobskater(unittest.TestCase):
    '''
    Tests integration of multiple components (high level functions)
    '''
    def test_basic_locals_arguments_no(self):
        '''will obfuscate locals, functions, arguments, but not module level identifiers and functions same'''
        #arrange
        code = """
def testOuter(*args, **kwargs):
    eval("1+1")
    arp=2
    def test(who,dat,man):
        arp2=3
        eval("2+2")
        return who+dat+man
    return test(*args, **kwargs)
        """

        #act
        obf = obfuscateString(code)
        print(obf)
        exec(obf, globals())

        #assert
        self.assertEqual(testOuter(2,3,4),9)

    def test_basic_locals_arguments_no(self):
        '''will not obfuscate kwargs'''
        #arrange
        code = """
def testOuter(babl=1, mopl=2, roopl=3):
    def test(map,cap,rap):
        return map*cap-rap
    return test(babl, mopl, roopl)
        """

        #act
        obf = obfuscateString(code)
        print(obf)
        exec(obf, globals())

        #assert
        self.assertEqual(testOuter(mopl=4, roopl=10),-6)

    def test_global(self):
        '''will not mess up on global'''
        #arrange
        code = """
who="wow"
def testGlobal():
    global who
    who=who if who else False
    return who
        """
        #If this fails, who would get obfuscated only inside
        #of test and it should return False or just raise an
        #Exception

        #act
        obf = obfuscateString(code)
        print(obf)
        exec(obf, globals())

        #assert
        self.assertEqual(testGlobal(),"wow")

    def test_docstrings(self):
        '''will remove docstrings'''
        #arrange
        code = """
def testDocString():
    '''
    Gottem
    '''
        """

        #act
        obf = obfuscateString(code)
        print(obf)

        #assert
        exec(obf, globals()) #This should not fail! It should be valid python code
        self.assertFalse(re.search(r"gottem", obf, re.I))

    def test_everythingDisabled(self):
        '''all settings off it wont remove docstring of var names'''
        #arrange
        code = """
def testDocString2():
    '''
    Gottem
    '''
    asdf = 2
        """

        #act
        obf = obfuscateString(code, 
            removeDocstrings=False,
            obfuscateNames=False)

        #assert
        print(obf)
        self.assertTrue(re.search(r"gottem", obf, re.I))
        self.assertTrue(re.search(r"asdf", obf, re.I))
        self.assertTrue(re.search(r"testDocString2", obf, re.I))
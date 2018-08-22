'''
Tests for frameUtils
'''
import unittest
import ast

from bobskater.frameUtils import Frame, FrameEntry

class TestFrame(unittest.TestCase):
    '''
    Tests Frame
    '''
    def test_addFrame(self):
        '''can add a frame to another frame'''
        #arrange
        f = Frame()
        f2 = Frame()

        #act
        f.addFrame(f2)

        #act/assert
        self.assertEqual(f2.parent, f)
        self.assertIn(f2, f.children)
        self.assertEqual(len(f.children), 1)
        self.assertEqual(len(f2.children), 0)

    def test_addEntry(self):
        '''can add a frame entry to another frame'''
        #arrange
        fe = FrameEntry("test")
        f = Frame()

        #act
        f.addEntry(fe)

        #act/assert
        self.assertEqual(f.ids["test"], fe)

    def test_getStack(self):
        '''can get a stack of frames up to root'''
        #arrange
        fs = [Frame() for _ in range(3)]
        #(Root) fs[0] -> fs[1] -> fs[2]
        for idx, f in enumerate(fs[1:]):
            fs[idx].addFrame(f)

        #act/assert
        self.assertEqual(fs[2].getStack(), [fs[0], fs[1], fs[2]])
        self.assertEqual(fs[1].getStack(), [fs[0], fs[1]])
        self.assertEqual(fs[0].getStack(), [fs[0]])

    def test_getScopedEntry(self):
        '''can find the first use of an identifier'''
        #arrange
        fs = [Frame() for _ in range(3)]
        #(Root) fs[0] -> fs[1] -> fs[2]
        for idx, f in enumerate(fs[1:]):
            fs[idx].addFrame(f)
        fe = FrameEntry("test")
        fe2 = FrameEntry("test")
        fs[0].addEntry(fe)
        fs[1].addEntry(fe2)

        #act/assert
        self.assertEqual(fs[2].getScopedEntry("test"), fe2)
        self.assertEqual(fs[2].getScopedEntry("not_there"), None)

    def test_getFrameStack(self):
        '''can get frames generated by given nodes'''
        #arrange
        fs = [Frame(source=ast.ClassDef(name="cls"+str(_))) for _ in range(4)]
        #(Root) fs[0] -> [fs[1] -> f[2], fs[3]]
        fs[0].addFrame(fs[1])
        fs[0].addFrame(fs[3])
        fs[1].addFrame(fs[2])

        #act
        frameStack = fs[0].getFrameStack([fs[1].source, fs[2].source])

        #assert
        self.assertEqual(frameStack, [fs[0], fs[1], fs[2]])

    def test_getAllIds(self):
        '''can get all ids in the current scope'''
        #arrange
        fs = [Frame() for _ in range(2)]
        #(Root) fs[0] -> fs[1]
        fs[0].addFrame(fs[1])
        fs[0].addEntry(FrameEntry(id="cls1"))
        fs[0].addEntry(FrameEntry(id="cls0"))

        #act
        ids = fs[1].getAllIds()

        #assert
        self.assertEqual(set(ids), set(["cls0", "cls1"]))
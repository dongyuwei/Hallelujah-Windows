import unittest
import sys
sys.path.append('./python') # python/python3/virtualenv/Scripts/python python/input_methods/hallelujah/test.py 

from ime_hallelujah import HallelujahTextService

class TestHallelujahTextService(unittest.TestCase):

    def setUp(self):
        client = {}
        self.text_service = HallelujahTextService(client)

    def test_loadTrie(self):
        # Test that trie is loaded 
        self.assertIsNotNone(self.text_service.trie)
    
    def test_loadWordsWithFrequency(self):
       # Test dictionary is loaded
       self.assertIsNotNone(self.text_service.wordsWithFrequencyDict)
       # Spot check some sample words
       self.assertIn('hello', self.text_service.wordsWithFrequencyDict)

    def test_loadPinyinData(self):
        # Test pinyin dictionary is loaded
        self.assertIsNotNone(self.text_service.pinyinDict)
        # Spot check some sample pinyin
        self.assertIn('nihao', self.text_service.pinyinDict)

    def test_getCandidates(self):
        candidates = self.text_service.getCandidates('hello')
        # Test candidates returned for valid word
        self.assertGreater(len(candidates), 0)
        self.assertEqual(candidates, ["hello ['hɛˈloʊ'] int. (打招呼)喂；你好", "hellos ['hellos*'] int. (打招呼)喂；你好", 'helloween   ', 'hellosoft   ', 'helloooo   '])
        
        # Test spelling suggestion
        candidates = self.text_service.getCandidates('hellp')        
        self.assertEqual(candidates, ['hellp   ', "help ['hɛlp'] v. 帮助；有助于；促进；擅自拿取；（不）能防止或避免某事物 n. 帮助", "hell ['hɛl'] n. 地狱；阴间；苦境；极大的痛苦 n. 究竟（用以加强语气） int. ", "hello ['hɛˈloʊ'] int. (打招呼)喂；你好", 'hellip   '])

    def test_getOutput(self):
        output = self.text_service.getOutput('world')
        self.assertEqual(output, 'world')

        # Test candidate selection
        self.text_service.setCompositionString('hello')
        self.text_service.setCandidateList(['hello', 'halo'])
        self.text_service.candidateCursor = 1
        output = self.text_service.getOutput('')
        self.assertEqual(output, 'halo')

if __name__ == '__main__':
    unittest.main()
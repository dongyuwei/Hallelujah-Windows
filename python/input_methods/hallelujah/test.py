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
        candidates = self.text_service.getCandidates('aosome')        
        self.assertEqual(candidates, [
            'aosome   ',
            "some ['səm'] adj. 一些；若干 adv. 大约；非常 pron. 一些(人、物)",
            "assume ['əˈsum'] vt. 假定；设想；承担；(想当然的)认为；假装",
            "awesome ['ˈɔsəm'] adj. 可怕的；表示敬畏的；了不起的；精彩的，绝妙的",
            'osom   ',
            "asme ['asme*'] abbr. 机场地面活动目标显示设备(=airport surface",
            "acme ['ˈækmi'] n. 顶点；极点"])

        candidates = self.text_service.getCandidates('kerrage')        
        self.assertEqual(candidates, [
            'kerrage   ',
            'perpage   ',
            "terrace ['ˈtɛrəs'] n. 平台；阳台；梯田 vt. 使成梯田；给 ... 建阳台",
            "peerage ['ˈpɪrəʤ'] n. 贵族；贵族爵位或头衔；贵族名册",
            "barrage ['bərɑʒ'] n. 弹幕；掩护炮火 n. 拦河坝 vt. 以密集火力进攻",
            "courage ['kərɪʤ'] n. 勇气；胆量",
            "carriage ['ˈkɛrəʤ'] n. 四轮马车；客车车厢；运输；运费；举止；托架",
            "karaoke ['kɛriˈoʊki'] n. 卡拉OK",
            "krug ['krəg'] n. 克鲁格"])

        # test for pinyin input
        candidates = self.text_service.getCandidates('pinyin')        
        self.assertEqual(candidates, [
            "pinyin ['pinyin*'] n. 拼音；汉语拼音",
            '拼音   ',
            'phonetic writing   ',
            'pinyin (Chinese romanization)   '])

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
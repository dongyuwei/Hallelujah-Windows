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
        self.assertEqual(len(candidates), 9)
        self.assertEqual(candidates, ["hello ['hɛˈloʊ'] int. (打招呼)喂；你好",
            "hellos ['hellos*'] int. (打招呼)喂；你好",
            'helloween   ',
            'hellosoft   ',
            'helloooo   ',
            "hell ['hɛl'] n. 地狱；阴间；苦境；极大的痛苦 n. 究竟（用以加强语气） int. ",
            "hill ['hɪl'] n. 小山；丘陵；山冈；斜坡 vt. 堆起；培土",
            "hall ['hɔl'] n. 大厅；礼堂",
            "holly ['ˈhɑli'] n. 冬青树 Holly. n. 霍莉(女子名)"
        ])

        candidates = self.text_service.getCandidates('test')
        self.assertEqual(candidates, ["test ['tɛst'] n. 考验；试验；测试 vt. 试验；测试；接受测验",
            "testing ['ˈtɛstɪŋ'] n. 测试 adj. 伤脑筋的；试验的 动词test的现在分",
            "tests ['tɛsts'] n. 考验；试验；测试 vt. 试验；测试；接受测验",
            "tested ['ˈtɛstɪd'] adj. 考验的；测试的 动词test的过去式和过去分词.",
            "testimonials ['tɛstɪˈmoʊniəlz'] n. 客户评价；证明书；感言；奖状（",
            "testimony ['ˈtɛstɪmoʊni'] n. 证明；证据",
            "testament ['ˈtɛstəmənt'] n. 证明；自白；[律]遗嘱；<古>圣约 Test",
            "tester ['ˈtɛstər'] n. 测试员；测试器；试用装；华盖；英国旧钱币（=teston",
            "testified ['ˈtɛstɪfaɪd'] v. 作证；证明；声明"
        ])

        candidates = self.text_service.getCandidates('sh')
        self.assertEqual(candidates, ["sh ['sh*'] int. 嘘(要别人不作声时用)",
            "should ['ʃʊd'] aux. 应该；可能；应当；竟然；将要",
            "she ['ʃi'] pron. 她（主格）",
            "shipping ['ˈʃɪpɪŋ'] n. 船运；发货；运输；乘船",
            "show ['ʃoʊ'] v. 证明；显现；展示；解说；指示；表示；表现；流露；带路；标示；描绘；陈",
            "shop ['ʃɑp'] n. 商店；车间 v. 逛商店；购物；买东西",
            "shopping ['ˈʃɑpɪŋ'] n. 购物；买东西 动词shop的现在分词形式.",
            "shall ['ʃæl'] aux. 将要；应该；一定；表示提供建议",
            "share ['ʃɛr'] vt. 分享，共享；分配；共有 vi. 分享 n. 一份；股份；分担；犁"
        ])
        
        # Test spelling suggestion
        candidates = self.text_service.getCandidates('aosome')        
        self.assertEqual(candidates, ['aosome   ',
            "some ['səm'] adj. 一些；若干 adv. 大约；非常 pron. 一些(人、物)",
            "assume ['əˈsum'] vt. 假定；设想；承担；(想当然的)认为；假装",
            "awesome ['ˈɔsəm'] adj. 可怕的；表示敬畏的；了不起的；精彩的，绝妙的",
            "asme ['asme*'] abbr. 机场地面活动目标显示设备(=airport surface",
            "acme ['ˈækmi'] n. 顶点；极点",
            "assam ['ɑˈsɑm'] n. (种于印度的)红茶 n. 阿萨姆(地方名)",
            "asim ['asim*'] (=American Society of Internal Medi",
            "asem ['asem*'] abbr. Application Specific Electron"
        ])

        candidates = self.text_service.getCandidates('kerrage')        
        self.assertEqual(candidates, ['kerrage   ',
            'perpage   ',
            "terrace ['ˈtɛrəs'] n. 平台；阳台；梯田 vt. 使成梯田；给 ... 建阳台",
            "peerage ['ˈpɪrəʤ'] n. 贵族；贵族爵位或头衔；贵族名册",
            "courage ['kərɪʤ'] n. 勇气；胆量",
            "carriage ['ˈkɛrəʤ'] n. 四轮马车；客车车厢；运输；运费；举止；托架",
            "karaoke ['kɛriˈoʊki'] n. 卡拉OK",
            "krug ['krəg'] n. 克鲁格",
            "crag ['crag*'] n. 峭壁；危岩"
        ])

        # test for pinyin input
        candidates = self.text_service.getCandidates('pinyin')        
        self.assertEqual(candidates, ["pinyin ['pinyin*'] n. 拼音；汉语拼音",
            '拼音   ',
            'phonetic writing   ',
            'pinyin (Chinese romanization)   ',
            "pinyon ['pinyon*'] n. 矮松 矮松果.",
            "pinion ['ˈpɪnjən'] n. 鸟翼；小齿轮 v. 剪断翼尖；绑住 ... 两臂",
            "panini ['pəˈnini'] n. 意大利帕尼尼三明治 Panini. n. 帕尼尼(公元前",
            "pennine ['pennine*'] n. 叶绿泥石",
            "penman ['ˈpɛnmən'] n. 笔者；画家；书法家"
        ])
        
        candidates = self.text_service.getCandidates('suanfa')        
        self.assertEqual(candidates, ['suanfa   ',
            "santa ['ˈsænə'] [美]=Santa Claus. n. 圣诞老人",
            "stanza ['ˈstænzə'] n. 诗节",
            'sana   ',
            '算法   ',
            "arithmetic ['ɛrɪθˈmɛtɪk'] n. 算术；计算 adj. 算术的",
            "algorithm ['ˈælgərɪðəm'] n. 算法",
            "samba ['ˈsɑmbə'] n. 桑巴舞(一种源自非洲的巴西交谊舞) v. 跳桑巴舞",
            "snafu ['sˈnæfu'] n. 混乱 adj. 混乱的 vt. 弄乱"
        ])

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
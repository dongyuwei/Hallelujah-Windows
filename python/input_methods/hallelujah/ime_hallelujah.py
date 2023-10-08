from keycodes import *
from textService import *
import os.path
import json
from heapq import nlargest
import marisa_trie

class HallelujahTextService(TextService):
    def __init__(self, client):
        TextService.__init__(self, client)
        self.dictPath = os.path.join(os.path.dirname(__file__), "dict")
        self.loadTrie()
        self.loadWordsWithFrequency()
        self.loadWordsWithFrequency()
        self.icon_dir = os.path.abspath(os.path.dirname(__file__))
    
    def loadTrie(self):
        trie = marisa_trie.Trie()
        trie.load(os.path.join(self.dictPath, "google_227800_words.bin"))
        print("hall keys:\n")
        print(trie.keys(u'test'))
        self.trie = trie
    
    def loadWordsWithFrequency(self):
        with open(os.path.join(self.dictPath, "words_with_frequency_and_translation_and_ipa.json"), encoding='utf-8') as f:
            self.wordsWithFrequencyDict = json.load(f)
    def loadPinyinData(self):
        with open(os.path.join(self.dictPath, "cedict.json"), encoding='utf-8') as f:
            self.pinyinDict = json.load(f)

    def onActivate(self):
        TextService.onActivate(self)
        self.customizeUI(candFontSize = 16, candPerRow = 9)
        self.setSelKeys("123456789")

    def onDeactivate(self):
        TextService.onDeactivate(self)

    def filterKeyDown(self, keyEvent):
        if not self.isComposing():
            if keyEvent.keyCode == VK_RETURN or keyEvent.keyCode == VK_BACK:
                return False
        return True

    def onKeyDown(self, keyEvent):
        print('hall keyEvent, charCode: ', keyEvent.charCode, '-- keyCode: ', keyEvent.keyCode)
        if (keyEvent.charCode >= ord('a') and keyEvent.charCode <= ord('z')) or (keyEvent.charCode >= ord('A') and keyEvent.charCode <= ord('Z')):
            prefix = self.compositionString  + chr(keyEvent.charCode).lower()
            suggestions = self.trie.keys(prefix)
            top27Candidates = nlargest(27, suggestions, key=lambda word: self.wordsWithFrequencyDict.get(word, {}).get('frequency', 0))
            if suggestions:
                self.setCandidateList(top27Candidates)
                self.setShowCandidates(True)
                return True
        
        # return False if not handled
        self.setCompositionString(self.compositionString + chr(keyEvent.charCode).lower())
        self.setCompositionCursor(len(self.compositionString))
        return False

    def onCommand(self, commandId, commandType):
        print("onCommand", commandId, commandType)

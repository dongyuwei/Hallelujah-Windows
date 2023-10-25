from keycodes import *
from textService import *
import os.path
import json
from collections import OrderedDict
from heapq import nlargest
import marisa_trie
import string
from autocorrect import Speller

class HallelujahTextService(TextService):
    def __init__(self, client):
        TextService.__init__(self, client)
        self.dictPath = os.path.join(os.path.dirname(__file__), "dict")
        self.loadTrie()
        self.loadWordsWithFrequency()
        self.loadPinyinData()
        self.icon_dir = os.path.abspath(os.path.dirname(__file__))
        self.spellchecker = Speller()
    
    def loadTrie(self):
        trie = marisa_trie.Trie()
        trie.load(os.path.join(self.dictPath, "google_227800_words.bin"))
        self.trie = trie
    
    def loadWordsWithFrequency(self):
        with open(os.path.join(self.dictPath, "words_with_frequency_and_translation_and_ipa.json"), encoding='utf-8') as f:
            self.wordsWithFrequencyDict = json.load(f)
    def loadPinyinData(self):
        with open(os.path.join(self.dictPath, "cedict.json"), encoding='utf-8') as f:
            self.pinyinDict = json.load(f)

    def onActivate(self):
        TextService.onActivate(self)
        self.customizeUI(candFontSize = 16, candPerRow = 1, candUseCursor=True, candFontName='MingLiu')
        self.setSelKeys("123456789")

    def onDeactivate(self):
        TextService.onDeactivate(self)

    # 使用者按下按鍵，在 app 收到前先過濾那些鍵是輸入法需要的。
    # return True，系統會呼叫 onKeyDown() 進一步處理這個按鍵
    # return False，表示我們不需要這個鍵，系統會原封不動把按鍵傳給應用程式
    def filterKeyDown(self, keyEvent):
        # 使用者開始輸入，還沒送出前的編輯區內容稱 composition string
        # isComposing() 是 False，表示目前沒有正在編輯
        if self.isComposing():
            return True
        # --------------   以下都是「沒有」正在輸入的狀況   --------------

        # 如果按下 Alt，可能是應用程式熱鍵，輸入法不做處理
        if keyEvent.isKeyDown(VK_MENU):
            return False

        # 如果按下 Ctrl 鍵
        if keyEvent.isKeyDown(VK_CONTROL):
            return False

        if keyEvent.isChar() and chr(keyEvent.charCode).isalpha():
            return True
        
        if keyEvent.isPrintableChar() and keyEvent.keyCode != VK_SPACE:
            return True

        # 其餘狀況一律不處理，原按鍵輸入直接送還給應用程式
        return False
    
    def getCandidates(self, prefix):
        input = prefix.lower()
        candidates = []
        suggestions = self.trie.keys(input)
        if len(suggestions) > 0:
            candidates = nlargest(10, suggestions, key=lambda word: self.wordsWithFrequencyDict.get(word, {}).get('frequency', 0))
        elif self.pinyinDict.get(input):
            candidates = self.pinyinDict.get(input)
        else:
            alternatives = self.spellchecker.get_candidates(input)
            alternatives.sort(key=lambda x: x[0], reverse=True)
            candidates = [word for freq, word in alternatives]
        candidates.insert(0, input)
        candidateList = list(OrderedDict.fromkeys(candidates).keys())[0:9]
        
        candidateList2 = []
        for word in candidateList:
            item = self.wordsWithFrequencyDict.get(word, {})
            ipa = item.get('ipa', ' ')
            word_ipa_translation = f"{word} [{ipa}] {self.getTranslationMessage(word)}"
            if word.lower().startswith(prefix.lower()):
                word_ipa_translation = f"{prefix + word[len(prefix):]} [{ipa}] {self.getTranslationMessage(word)}"
            candidateList2.append(word_ipa_translation[0:50])  

        return candidateList2
    
    def inputWithCandidates(self, input):
        self.setCompositionString(input)
        self.setCompositionCursor(len(input))
        self.setCandidateList(self.getCandidates(input))
        self.setShowCandidates(True)

    def clear(self):
        self.setCandidateList([])
        self.setCandidateCursor(0)
        self.setShowCandidates(False)

        self.setCompositionString("")
        self.setCompositionCursor(0)
        

    def onDeactivate(self):
        self.setCompositionString(self.compositionString)
        self.clear()

    def getOutput(self, chrStr):
        output = self.compositionString
        if self.candidateCursor <= len(self.candidateList) - 1:
            candidate = self.candidateList[self.candidateCursor]
            if candidate:
                word, ipa = candidate.split(' ', 1)
                output = word
        return output + chrStr
        
    def onKeyDown(self, keyEvent):
        print('halle keyEvent, charCode: ', keyEvent.charCode, '-- keyCode: ', keyEvent.keyCode)
        charStr = chr(keyEvent.charCode)
            
        # handle candidate selection
        if self.showCandidates:
            if keyEvent.isKeyDown(VK_CONTROL):
                self.setCommitString(self.compositionString)
                self.clear()
                return False
            if keyEvent.keyCode == VK_ESCAPE:
                self.setCommitString(self.compositionString)
                self.clear()
                return True
            elif not keyEvent.isKeyDown(VK_SHIFT) and (keyEvent.keyCode >= ord('1') and keyEvent.keyCode <= ord('9')):
                index = keyEvent.keyCode - ord('1')
                print("halle", index, charStr, self.candidateList)
                if index < len(self.candidateList):
                    candidate = self.candidateList[index]
                    word, ipa = candidate.split(' ', 1)
                    self.setCommitString(word)
                    self.clear()
                    return True
        
        # handle normal text input
        if not self.isComposing():
            if keyEvent.keyCode == VK_RETURN or keyEvent.keyCode == VK_BACK:
                return False
        
        if keyEvent.keyCode == VK_RETURN:
            self.setCommitString(self.getOutput(""))
            self.clear()
            return True
        elif keyEvent.keyCode == VK_BACK:
            if len(self.compositionString) > 1:
                input = self.compositionString[:-1]
                self.inputWithCandidates(input)
            else:
                self.setCommitString("")
                self.clear()
            return True
        elif charStr in string.punctuation or keyEvent.keyCode == VK_SPACE: #標點符號或者空白鍵
            self.setCommitString(self.getOutput(charStr))
            self.clear()
            return True
        elif charStr.isalpha():  # 英文字母 A-Z
            input = self.compositionString  + charStr
            self.inputWithCandidates(input)
            return True
        elif keyEvent.keyCode == VK_LEFT or keyEvent.keyCode == VK_UP:
            i = self.candidateCursor - 1
            if i >= 0:
                self.setCandidateCursor(i)
            return True
        elif keyEvent.keyCode == VK_RIGHT or keyEvent.keyCode == VK_DOWN:
            i = self.candidateCursor + 1
            if i <= len(self.candidateList) - 1:
                self.setCandidateCursor(i)
            return True
        return False
    
    def getTranslationMessage(self, word):
        translation = self.wordsWithFrequencyDict.get(word.lower(), {}).get('translation', [])
        return " ".join(translation)

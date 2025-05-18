from keycodes import *
from textService import *
import os.path
import sqlite3
import orjson
from collections import OrderedDict
import string
from autocorrect import Speller
from pyphonetics import FuzzySoundex
import textdistance
import os
import shutil
from loguru import logger
import cProfile

user_folder = os.environ['userprofile']
log_dir = r"{}\AppData\Local\PIME\Log".format(user_folder) 
log_file = os.path.join(log_dir, "PIME-hallelujah.log")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logger.add(log_file)

init_db_path = os.path.join(os.path.join(os.path.dirname(__file__), "dict"), 'words_with_frequency_and_translation_and_ipa.sqlite3')
db_path = r"{}\AppData\Local\PIME\PIME-hallelujah.sqlite3".format(user_folder)
# we must copy the sqlite db to user folder with read && write permission(wal,shm)
shutil.copy2(init_db_path, db_path)

fuzzySoundex = FuzzySoundex()
def damerau_levenshtein_distance(word, input_word):
    return textdistance.damerau_levenshtein(word, input_word)

class PersistentImeService:
    def __init__(self):
        self.dictPath = os.path.join(os.path.dirname(__file__), "dict")
        self.icon_dir = os.path.abspath(os.path.dirname(__file__))
        if os.getenv('TEST_ENV') == 'true':
            pr = cProfile.Profile()
            pr.enable()
            self.init()
            pr.disable()
            pr.print_stats(sort='time')
        else:
            self.init()

    def init(self):
        self.init_db_connection()
        self.loadPinyinData()
        self.loadFuzzySoundexEncodedData()
        self.get_user_defined_substitutions()
        self.spellchecker = Speller()
    
    def init_db_connection(self):
        with sqlite3.connect(db_path) as conn:
            self.db_connection = conn
    
    def loadPinyinData(self):
        with open(os.path.join(self.dictPath, "cedict.json"), 'rb') as f:
            self.pinyinDict = orjson.loads(f.read())

    def get_user_defined_substitutions(self):
        json_file_path = os.path.join(os.environ['USERPROFILE'], 'hallelujah.json')
        try:
            with open(json_file_path, 'rb') as f:
                self.substitutions = orjson.loads(f.read())
        except FileNotFoundError:
            print(f"File {json_file_path} not found.")
            self.substitutions = {}
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            self.substitutions = {}
    
    # get phonetics match
    def loadFuzzySoundexEncodedData(self):
        with open(os.path.join(self.dictPath, "fuzzy_soundex_encoded_words.json"), 'rb') as f:
            self.fuzzySoundexEncodedDict = orjson.loads(f.read())

imeService = PersistentImeService()

class HallelujahTextService(TextService):
    def __init__(self, client):
        TextService.__init__(self, client)
        # Only load and build the dict/trie once! 因为每次切换输入法都会导致HallelujahTextService重新初始化。
        self.__dict__.update(imeService.__dict__)
        self.showIPA = True

    def onActivate(self):
        TextService.onActivate(self)
        self.customizeUI(candFontSize = 14, candPerRow = 1, candUseCursor=True, candFontName='MingLiu')
        self.setSelKeys("123456789")

    def onDeactivate(self):
        self.db_connection.close()
        TextService.onDeactivate(self)

    # 使用者按下按键，在 app 收到前先处理输入法需要处理的。
    # return True，系统会调用 onKeyDown() 进一步处理此按键。
    # return False，表示输入法不需要处理，系统会把事件传递给应用程序处理。
    def filterKeyDown(self, keyEvent):
        # 使用者開始輸入，還沒送出前的編輯區內容稱 composition string
        # isComposing() 是 False，表示目前沒有正在編輯
        if self.isComposing():
            return True
        # --------------   以下都是「沒有」正在輸入的狀況   --------------

        # 如果按下 Alt，可能是應用程式熱鍵，輸入法不做處理
        if keyEvent.isKeyDown(VK_MENU):
            return False

        # 如果按下的不是 ctrl+` 则输入法不做处理
        if keyEvent.isKeyDown(VK_CONTROL) and keyEvent.keyCode != VK_OEM_3:
            return False

        if keyEvent.isChar() and chr(keyEvent.charCode).isalpha():
            return True
        
        if keyEvent.isPrintableChar() and keyEvent.keyCode != VK_SPACE:
            return True

        # 其餘狀況一律不處理，原按鍵輸入直接送還給應用程式
        return False
    
    def getSuggestionOfSpellChecker(self, input):
        alternatives = self.spellchecker.get_candidates(input)
        alternatives.sort(key=lambda x: x[0], reverse=True)
        candidates = [word for freq, word in alternatives]
        # If the input word is longer than 3 characters, add phonetic and Pinyin suggestions
        if len(input) > 3:
            phonetic_candidates = []
            try:
                encoded_key = fuzzySoundex.phonetics(input)
                phonetic_candidates = self.fuzzySoundexEncodedDict.get(encoded_key, [])
                phonetic_candidates.sort(key=lambda word: damerau_levenshtein_distance(word, input))
            except Exception as e:
                logger.error(f"Error generating phonetic key for '{input}': {e}")
                phonetic_candidates = []  # Ensure phonetic_candidates is an empty list if an error occurs

            pinyin_candidates = self.pinyinDict.get(input, [])
            candidates = candidates[:3] + pinyin_candidates[:3] + phonetic_candidates
        return candidates
    
    def query_candidates_by_prefix(self, prefix):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT word FROM words WHERE word LIKE ? ORDER BY frequency DESC limit 10', (prefix + '%',))
        results = cursor.fetchall()
        candidates = []
        for result in results:
            candidates.append(result[0])
        return candidates 
    
    # spell check results also need translations_and_ipa
    def get_translations_and_ipa(self, word_list):
        cursor = self.db_connection.cursor()
        placeholders = ', '.join(['?'] * len(word_list))
        query = f"""
        SELECT word, translation, ipa 
        FROM words 
        WHERE word IN ({placeholders})
        """
        cursor.execute(query, word_list)
        results = cursor.fetchall()
        translations_and_ipa = {word: (translation.replace('|', ' '), ipa) for word, translation, ipa in results}
        return translations_and_ipa
    
    def getCandidates(self, prefix):
        input = prefix.lower()
        candidates = self.query_candidates_by_prefix(input)
        candidates = candidates + self.getSuggestionOfSpellChecker(input)
        
        candidates.insert(0, input)
        candidateList = list(OrderedDict.fromkeys(candidates).keys())[0:9]
        
        candidateList2 = []
        if self.substitutions.get(input):
            candidateList2.append(self.substitutions.get(input)) #自定义短语优先级最高
        translations_and_ipa = self.get_translations_and_ipa(candidateList)
        for word in candidateList:
            translation, ipa = translations_and_ipa.get(word, ('', ''))
            ipa2 = f"{[ipa]}" if ipa else ' '
            word_ipa_translation = f"{word} {ipa2} {translation}"
            if not self.showIPA:
                word_ipa_translation = word
            if word.lower().startswith(prefix.lower()):
                if self.showIPA:
                    word_ipa_translation = f"{prefix + word[len(prefix):]} {ipa2} {translation}"
                else:
                    word_ipa_translation = f"{prefix + word[len(prefix):]}"
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
            output = self.getOutputFromCandidate(candidate)
        return output + chrStr
    def getOutputFromCandidate(self, candidate):
        word = ''
        if candidate:
            if '[' in candidate:
                word, ipa = candidate.split('[', 1)
            else:
                word = candidate
        return word.strip()
        
    def onKeyDown(self, keyEvent):
        # Check for Ctrl+` key combination (VK_OEM_3 is the virtual key code for `)
        if keyEvent.isKeyDown(VK_CONTROL) and keyEvent.keyCode == VK_OEM_3:
            logger.info("Ctrl+` pressed")
            self.showIPA = not self.showIPA
            self.inputWithCandidates(self.compositionString)
            return True  # Key handled, prevent further processing
        
        # print('halle keyEvent, charCode: ', keyEvent.charCode, '-- keyCode: ', keyEvent.keyCode)
        charStr = chr(keyEvent.charCode)

        # handle candidate selection
        if self.showCandidates:
            if keyEvent.keyCode == VK_ESCAPE:
                self.setCommitString(self.compositionString)
                self.clear()
                return True
            elif not keyEvent.isKeyDown(VK_SHIFT) and (keyEvent.keyCode >= ord('1') and keyEvent.keyCode <= ord('9')):
                index = keyEvent.keyCode - ord('1')
                # print("halle", index, charStr, self.candidateList)
                if index < len(self.candidateList):
                    candidate = self.candidateList[index]
                    word = self.getOutputFromCandidate(candidate)
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
        elif charStr.isdigit():
            self.setCommitString(charStr)
            self.clear()
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

import re
import random

class PatternItem:
    #パターン辞書1行の情報を保持するクラス
    
    SEPARATOR = '^((-?\d+)##)?(.*)$'
    
    def __init__(self,pattern,phrases):
        
        self.initModifyAndPattern(pattern)
        self.initPhrases(phrases)
        
    def initModifyAndPattern(self,pattern):
        
        #辞書パターンの部分にSEPARATORをパターンマッチさせる
        m = re.findall(PatternItem.SEPARATOR, pattern)
        #機嫌変動値を保持するインスタンス変数を0で初期化
        self.modify = 0
        
        
        #マッチ結果からパターン部分を取り出して
        #マッチ結果の整数の部分がからでなければ機嫌変動値をself.modifyに代入
        if m[0][1]:
            self.modify = int(m[0][1])
        
        #マッチ結果からパターン部分を取り出してself.patternに代入
        self.pattern = m[0][2]
        
        
    def initPhrases(self,phrases):
        #self.phrases(dicのlist)の初期化を行う
        
        #リスト型のインスタンス変数
        self.phrases = []
        #dic型のローカル変する
        dic = {}
        
        #引数で渡された応答フレーズグループを'|'で分割し
        #１個の応答フレーズに対してSEPARETORをパターンマッチさせる
        #{'need' : 必要機嫌値, 'phrase' : '応答フレーズ１個'}を作成し
        #リストself.phrasesに格納する
        for phrase in phrases.split('|'):
            #１個の応答フレーズに対してパターンマッチさせる
            m = re.findall(PatternItem.SEPARATOR, phrase)
            #'need'キーの値を必要機嫌値m[0][1]にする
            #'phrase'キーの値を応答フレーズm[0][2]にする
            dic['need'] = 0
            
            if m[0][1]:
                dic['need'] = int(m[0][1])
                
            dic['phrase'] = m[0][2]
            #作成した辞書をリストphrasesに追加
            self.phrases.append(dic.copy())
        
    
    def match(self, str):
        #ユーザのメッセージにself.pattern(パターン辞書1行の正規表現のパターン)
        #がマッチするのか調べる
        
        return re.search(self.pattern, str)
    
    
    def choice(self, mood):
        #現在の機嫌値と必要機嫌値を比較し、適切な応答フレーズを返す
        
        choices = []
        #self.phrasesが保持する'need''phrase'の辞書を反復処理する
        for p in self.phrases:
            #self.phrasesの'need'キーの数値とパラメーターmoodをsuitable()に渡す
            #必要機嫌値による条件をクリア(True)であれば、
            #対になっている応答フレーズをchoicesリストに追加する
            if (self.suitable(p['need'],mood)):
                choices.append(p['phrase'])
        
        #choicesリストがからであればNoneを返す
        if (len(choices) == 0):
            return None
        
        #choicesリストからランダムに応答フレーズを抽出して返す　
        return random.choice(choices)

    def suitable(self,need,mood):
        #現在の機嫌値が必要機嫌値の条件を満たすかを判定
        
        #必要機嫌値が0であればTrueを返す
        if (need == 0):
            return True
        #必要機嫌値がプラスの場合は機嫌値が必要機嫌値を超えているか判定
        elif (need > 0):
            return (mood > need)
        #応答例の数値がマイナスの場合は機嫌値が下回っているか判定
        else:
            return (mood < need)
        
    def add_phrase(self,phrase):
        #ユーザのメッセージの形態素が既存のパターンとマッチした場合に
        #Dictionaryのstudy_pattern()メソッどから呼ばれる
        
        for p in self.phrases:
            if p['phrase'] == phrase:
                return
        
        self.phrases.append({'need' : 0 ,'phrase' : phrase})
    
    def make_line(self):
        #パターン辞書1行ヴンのデータを作る
        
        
        #機嫌変動値##パターン　　をつるく
        pattern = str(self.modify) + '##' + self.pattern
        #応答フレーズグループ用のリスト
        pr_list = []
        
        #応答フレーズのグループを作成する
        
        for p in self.phrases:
            #必要機嫌値##応答フレーズ　　を作ってリストに追加する
            pr_list.append(str(p['need']) + '##' + p['phrase'])
            
        #機嫌変動値##パターン文字列[TAB]　　に|で区切った
        #必要機嫌値##応答フレーズ　　のグループを連結して返す
        return pattern + '\t' + '|'.join(pr_list)
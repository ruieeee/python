import responder
import random
import dictionary
import analyzer
import requests,webbrowser,bs4

#urlエンコード
import urllib.parse

class Rear(object):
    
    def __init__(self,name):
        self.name = name
        
        self.dictionary = dictionary.Dictionary()
        self.emotion = Emotion(self.dictionary.pattern)
        self.res_repeat = responder.RepeatResponder('Repeat?')
        self.res_random = responder.RandomResponder('Random', self.dictionary.random)
        self.res_pattern = responder.PatternResponder(
            'Pattern or Random', self.dictionary.pattern,self.dictionary.random)
        self.res_template = responder.TemplateResponder(
            'Template',self.dictionary.template, self.dictionary.random)
        
        
    def dialogue(self, input):
        #応答オフジェクトのresponse()を呼び出して応答文字列を取得する
        
        self.emotion.update(input)
        
        #ユーザーからのメッセージを解析
        parts = analyzer.analyze(input)
        
        x = random.randint(1,100)
        
        if x <= 40:
            self.responder = self.res_pattern
            
        elif 40 < x <= 90:
            self.responder = self.res_template
            
        elif 90 < x <= 95:
            self.responder = self.res_random
            
        else:
            self.responder = self.res_repeat
        
        #機嫌値を確認したいときに使う(コンソールでmoodの値を出力)
        #print(self.emotion.mood)
        
        
        #応答フレーズを生成
        resp = self.responder.response(input, self.emotion.mood,parts)
        #学習メソッドを呼ぶ
        #応答フレーズを生成する前に学習してしまうと、ユーザが入力したばかりのフレーズを
        #おうむ返しする可能性がある
        self.dictionary.study(input,parts)
        #応答フレーズを返す
        return resp
    
    def save(self):
        #Dictionaryのsave()を呼ぶ中継メソッド
        self.dictionary.save()
    
    def Map(self):
        webbrowser.open('https://www.google.co.jp/maps')
    def map_search(self,value):
        s,word = value.split(':')
        parameter = urllib.parse.quote(word)
        webbrowser.open('http://maps.google.co.jp/maps?q=' + ''.join(parameter))
        
        return word + 'をgoogleマップで検索!'
    
    def search(self,value):
        s,word = value.split(':')
        
        res = requests.get('https://google.com/search?q=' + ' '.join(word))

        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text)
        print(soup)
        link_elems = soup.select('.kCrYT > a')

        webbrowser.open('http://google.com' + link_elems[0].get('href'))
        
        return word + 'を検索!'
    
    def get_responder_name(self):
        
        return self.responder.name
    
    def get_name(self):
        
        return self.name

class Emotion:
    #感情モデル
    
    #機嫌値の上限、下限、回復値をクラス変数として定義
    MOOD_MIN = -15
    MOOD_MAX = 15
    MOOD_RECOVERY = 0.5
    
    def __init__(self, pattern):
        #Dictionaryオブジェクトのpatternをインスタンス変数dictionaryに格納
        
        self.pattern = pattern
        self.mood = 0
        
    def update(self, input):
        #機嫌値変動メソッド　　　対話のたびに呼びだ戯れる
        if self.mood < 0:
            self.mood += Emotion.MOOD_RECOVERY
        elif self.mood > 0:
            self.mood -= Emotion.MOOD_RECOVERY
        
        
        #パターン辞書の各行の正規表現をユーザのメッセージに繰り返しパターンマッチさせる
        #マッチした場合はajust_mood()で機嫌値を変動させる
        for ptn_item in self.pattern:
            if ptn_item.match(input):
                self.adjust_mood(ptn_item.modify)
                break
        
    
    def adjust_mood(self, val):
        #機嫌値を増減させるメソッド
        #モードの値を機嫌変動値によって増減する
        self.mood += int(val)
        #maxとminと比較して、機嫌値が取り得る範囲に収める
        if self.mood > Emotion.MOOD_MAX:
            self.mood = Emotion.MOOD_MAX
        elif self.mood < Emotion.MOOD_MIN:
            self.mood = Emotion.MOOD_MIN
            
            
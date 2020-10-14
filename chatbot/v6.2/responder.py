import random
import re
import analyzer

class Responder(object):

    def __init__(self, name):
        self.name = name
            
    def response(self, input,mood,parts):    #オーバーライドを前提としたrespons()メソッド
        return ''
        
class RepeatResponder(Responder):
    #おうむ返しのためのサブクラス
    def __init__(self, name):
        super().__init__(name)
        
    def response(self, input,mood,parts):
        #response()をオーバーライド、おうむ返しの返答をする
        
        return '{}って何？'.format(input)
    
    
class RandomResponder(Responder):
    #ランダムな応答のためのサブクラ
    def __init__(self, name, dic_random):
        '''Responderオブジェクトの名前をnameに格納、
        ランダムに抽出するメッセージを格納したリストを作成する
        スーパークラスの初期化メソッドを読んでResponder名をnameに格納
        '''
        super().__init__(name)
        self.random = dic_random
        
    def response(self,input, mood):
        #response()をオーバーライド、ランダムな応答を返す
        return random.choice(self.random)
    
class PatternResponder(Responder):
    #パターンに反応するサブクラス
    def __init__(self, name,dic_pattern,dic_random):
        '''スーパークラスの__init__()にnameを渡し
        Dictionaryオブジェクトをインスタンス変数に格納する
        '''
        super().__init__(name)
        self.pattern = dic_pattern
        self.random = dic_random
        
    
    def response(self,input,mood,parts):
        #パターンにマッチした場合に応答文字列を作って返す
        
        resp = None
        #patternリストのPatternItemオブジェクトに対して反復処理を行う
        for ptn_item in self.pattern:
            #パターン辞書1行の正規表現がユーザーのメッセージにマッチするか試みる
            #マッチしたらMatchオブジェクト、そうでなければNoneが返ってくる
            m = ptn_item.match(input)
            #マッチした場合は機嫌値moodを引数にしてchoice()を実行
            if m:
                resp = ptn_item.choice(mood)
               #choice()の戻り値がNone出ない場合は
               #応答例の中の%match%をインプットされた文字列内の
               #マッチされた文字列に置き換える
            if resp != None:
                return re.sub('%match%',m.group(),resp)
            
        #パターンマッチしない場合はランダム辞書から返す
        return random.choice(self.random)


class TemplateResponder(Responder):
    #テンプレートに反応するためのサブクラス
    
    
    def __init__(self,name,dic_template,dic_random):
        
        super().__init__(name)
        self.template = dic_template
        self.random = dic_random
        
    def response(self, input, mood, parts):
        #テンプレートを使用して応答フレーズを生成する
        
        #インプット文字列の名詞の部分のみを保持するリスト
        keywords = []
        #解析結果partsの「文字列」　ー>word,　「品詞情報」->partに順次格納
        for word,part in parts:
            #名詞であれば形態素をkeywordsに追加
            if analyzer.keyword_check(part):
                keywords.append(word)
            
            count = len(keywords)
            #keywordsリストに1つ以上の名詞が存在し
            #名詞の数に対応する'%noun%'を持つテンプレートが存在すれば
            #テンプレートを利用して応答フレーズを生成する
            if (count > 0) and (str(count) in self.template):
                #テンプレートリストからランダムに１個抽出
                resp = random.choice(
                    self.template[str(count)]
                    )
                #keywordsから取り出した名詞でテンプレートの'%noun%'を書き換える
                for word in keywords:
                    resp = resp.replace('%noun%',#書き換える文字
                                        word,   #書き換え後の文字列
                                        1       #書き換える回数
                                        )
                return resp
        
        #メッセージに名詞が存在しない、または適切なテンプレートが存在しない場合は
        #ランダム辞書から返す
        return random.choice(self.random)
        
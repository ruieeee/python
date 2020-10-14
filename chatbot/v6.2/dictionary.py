import patternItem
import re
import analyzer

class Dictionary(object):
    '''
    ランダム辞書とパターン辞書を開き、データをインスタンス変数に格納する
    '''
    def __init__(self):
        
        #ランダム辞書
        self.random = self.makeRandomList()
        #パターン辞書
        self.pattern = self.makePatternDictionary()
        #テンプレート辞書を作成
        self.template = self.makeTemplateDictionary()
        
    def makeRandomList(self):
        '''ランダム辞書ファイルのデータを読み込んで
        random　に格納する
        '''
    
        rfile = open('dics/random.txt', 'r', encoding = 'utf_8')
        
        r_lines = rfile.readlines()
        rfile.close()
        
        randomList = []
        
        for line in r_lines:
            str = line.rstrip('\n')
            if (str != ''):
                randomList.append(str)
        return randomList
    
    
    def makePatternDictionary(self):
         
        #パターン辞書ファイルのデータを読み込んでpattern　に格納する
        pfile = open('dics/pattern.txt', 'r', encoding = 'utf_8')
        
        p_lines = pfile.readlines()
        pfile.close()
        
        new_lines = []
        for line in p_lines:
            str = line.rstrip('\n')
            if(str != ''):
                new_lines.append(str)
        
        #パターン辞書の行数だけ繰り返す
        patternItemList= []
        #1行をタブで切り分けて辞書オブジェクトに格納
        #'pattern'キー:正規表現のパターん
        #'phrases'キー:応答例

        for line in new_lines:
            ptn,prs = line.split('\t')#TABで切り分けてptn,prsに格納
            patternItemList.append(
                patternItem.PatternItem(ptn,prs))
        return patternItemList
    
    def makeTemplateDictionary(self):
        #テンプレート辞書ファイルのデータを読み込んで
        # %noun%の出現回数:テンプレートの文字列　の辞書を作る
        
        tfile = open('dics/template.txt','r',encoding = 'utf_8')
        t_lines = tfile.readlines()
        tfile.close()
        
        #末尾の改行と空白文字を取り除いてリストに格納
        new_t_lines = []
        for line in t_lines:
            str = line.rstrip('\n')
            if(str!=''):
                new_t_lines.append(str)
        
        #テンプレート辞書の改行をタブで切り分けて
        #%noun%の出現回数をキー、テンプレートの文字列をその値にした辞書要素を作る
        templateDictionary = {}
        for line in new_t_lines:
            count,tempstr = line.split('\t')
            
            if not count in templateDictionary:
                templateDictionary[count] = []
            templateDictionary[count].append(tempstr)
        
        return templateDictionary
        
    
    def study(self,input,parts):
        #ユーザの発言を学習
        
        #インプット文字列末尾の改行を取り除く
        input = input.rstrip('\n')
        
        #ユーザーメッセージを引数にして、ランダム辞書に登録するメソッドを呼ぶ
        self.study_random(input)
        #ユーザーメッセージと解析結果を引数にしてパターン辞書に登録するメソッドを呼ぶ
        self.study_pattern(input,parts)
        
        #解析結果を引数にして、テンプレート辞書に登録するメソッドを呼ぶ
        self.study_template(parts)
        
    def study_random(self,input):
        #ユーザの発言をランダム辞書に書き込む
        
        if not input in self.random:
            self.random.append(input)
    
    def study_pattern(self,input,parts):
        #ユーザの発言を学習し、パターン辞書へ書き込む
        
        
        for word, part in parts:
            
            #形態素の品詞情報が指定の品詞にマッチした時の処理
            if analyzer.keyword_check(part):
                depend = None #PatternItemオブジェクトを保持する変数
                #マッチングしたユーザのメッセージの形態素が、パターン辞書の
                #パターン部分に一致するか、繰り返しパターンマッチを試す
                for ptn_item in self.pattern:
                    #パターン辞書のパターン部分とマッチしたら形態素とメッセージ
                    #新規のパターン/応答フレーズとして登録する処理に進む
                    if re.search(ptn_item.pattern, word):
                        #パターン辞書1行データのオブジェクトを変数で処理
                        depend = ptn_item
                        #マッチしたらこれ以上のパターンマッチは行わない
                        break
                #ユーザメッセージの形態素がパターン辞書のパターン部分と
                #マッチしていたら、対応する応答フレーズグループの最後にユーザメッセージを
                #追加する
                if depend:
                    depend.add_phrase(input)
                else:
                    #パターン辞書に存在しない形態素であれば
                    #新規のPatternItemオブジェクトを生成してpatternリストに追加する
                    self.pattern.append(
                        patternItem.PatternItem(word, input))
    
    def study_template(self,parts):
        #ユーザの発言を学習、テンプレート辞書オブジェクトに登録
        
        tempstr = ''
        count = 0
        
        #ユーザメッセージの形態素が名詞であれば形態素を'%noun%'に書き換え
        #そうでなければ元の形態素のままにして、「やっぱり%noun%だね」のような
        #パターン文字列を作る
        
        for word, part in parts:
            #形態素が名刺であればwordに'%noun%'を代入し、カウンター 1加算
            if (analyzer.keyword_check(part)):
                word = '%noun%'
                count += 1
            #形態素または'%noun%'を追加する
            tempstr += word
        
        #'%noun%'が存在する場合のみ、辞書self.templateに追加する処理に進む
        if count > 0:
            count = str(count)
            #テンプレート文字列の'%noun%'の出現回数countが
            #self.templateのキーとして存在しなければ
            #countの値をキー、空のリストをその値としてself.templateに追加
            if not count in self.template:
                self.template[count] = []
            
            #処理中のテンプレート文字列tempstrが、self.templateのcountを
            #キーとするリスト内に存在しなければ、リストにtempstrを追加する
            if not tempstr in self.template[count]:
                self.template[count].append(tempstr)
    
    
    def save(self):
        #self.random,self.pattern,self.templateの内容を
        #それぞれに書き込む
        
        #各フレーズの末尾に改行を追加する
        for index, element in enumerate(self.random):
            self.random[index] = element + '\n'
        
        #ランダム辞書に書き込む
        with open('dics/random.txt', 'w', encoding = 'utf_8') as f:
            f.writelines(self.random)
        
        pattern = []
        
        #パターン辞書のすべてのPatternItemオブジェクトから
        #辞書ファイル1行のフォーマットを繰り返し作成する
        for ptn_item in self.pattern:
            #make_line()で作成したファーマットの末尾に改行を追加
            pattern.append(ptn_item.make_line() + '\n')
        #パターン辞書ファイルに書き込む
            with open('dics/pattern.txt', 'w', encoding = 'utf_8') as f:
                f.writelines(pattern)
        
        #テンプレート辞書に書き込み
        templist = []
        
        for key, val in self.template.items():
            for v in val:
                templist.append(key + '\t' + v + '\n')
        
        templist.sort()
        
        with open('dics/template.txt', 'w', encoding = 'utf_8') as f:
            f.writelines(templist)
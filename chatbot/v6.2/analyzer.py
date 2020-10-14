import re
import janome.tokenizer

def analyze(text):
    #形態素解析を行う関数
    
    t = janome.tokenizer.Tokenizer()#Tokenizerのオブジェクトを生成
    tokens = t.tokenize(text)       #形態素解析を実行
    result = []                     #解析結果の形態素と品詞を格納するリスト
    
    #リストからTokenオブジェクトを1つずつ取り出す
    for token in tokens:
        result.append(
            [token.surface,             #形態素を取得
             token.part_of_speech])     #品詞情報を取得
    return(result)
    #[['phthon','名詞,固有名詞,組織,*'],…]

def keyword_check(part):
    #品詞が名詞であるか調べる関数
    
    return re.match(
        '名詞,(一般|固有名詞|サ変接続|形容動詞語幹)',part
        )

    
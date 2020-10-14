from PyQt5 import QtWidgets
from PyQt5 import QtGui
import qi_rearUI
import rear
import datetime
import re

class MainWindow(QtWidgets.QMainWindow):
    '''QtWidgets.QMainWindowを継承したサブクラス
    UI画面の構築を行う
    '''
    
    def __init__(self):
        '''
        スーパクラスの__init__を呼び出す
        rearオブジェクトを生成してself.rearに格納
        ラジオボタンの状態を保持する変数をTrueに初期化
        setupUi()を実行してUI画面を構築する
        '''
        
        super().__init__()
        self.rear = rear.Rear('rear')           #rearオブジェクトの生成
        self.action = True                      #ラジオボタンの初期化
        self.ui = qi_rearUI.Ui_MainWindow()     #Ui_MainWindowオブジェクトの生成
        #setupUi()で画面を構築、MainWindow自信を引数にすることが必要
        self.ui.setupUi(self)
        self.log = []                           #ログリストを用意
        
    def putlog(self, str):
        #対話ログをリストに追加するメソッド
        
        #QListWidgetクラスのaddItem()でログをリストに追加する
        self.ui.listWidgetLog.addItem(str)
        
        #ユーザからのメッセージ、リアの応答に改行をつけてlogに追加
        self.log.append(str + '\n')
        
    def prompt(self):
        #リアーのプロンプトを作るメソッド
        
        p = self.rear.get_name()
        #「Responderを表示」ガオンならオブジェクト名を付加する
        if self.action == True:
            p += ':' + self.rear.get_responder_name()
            
        return p + '>'
    
    def change_looks(self):
        #機嫌値によってリアの表情をかえるメソッド
        
        #応答フレーズを返す直前のリアの機嫌値を取得
        em = self.rear.emotion.mood
        
        if -5 <= em <= 5:
            self.ui.labelShowImg.setPixmap(QtGui.QPixmap(":/re/talk.gif"))
        
        elif -10 <= em < -5:
            self.ui.labelShowImg.setPixmap(QtGui.QPixmap(":/re/empty.gif"))
            
        elif -15 <= em < -10:
            self.ui.labelShowImg.setPixmap(QtGui.QPixmap(":/re/angry.gif"))
            
        elif 5 <= em < 15:
            self.ui.labelShowImg.setPixmap(QtGui.QPixmap(":/re/happy.gif"))
        
    
    def writeLog(self):
        #ログを更新日時とともにログファイルに書き込む
        
        #ログタイトルと更新日時のテキストを作成
        #日時は2020-01-01 00:00::00の書式
        now = 'Rear System Dialogue Log'\
            + datetime.datetime.now().strftime('%Y-%m-%d %H:%m::%S')\
            + '\n'
            
        #リストlogの先頭要素として更新日時を追加
        self.log.insert(0, now)
        
        #logのすべての要素をログファイルへ書き込む
        with open('dics/log.txt', 'a', encoding = 'utf_8') as f:
            f.writelines(self.log)
            
    def buttonTalkSlot(self):
        #話す　ボタンのイベントハンドラー
        #rearクラスのdialogue()を実行して応答メッセージを取得
        #入力文字列および応答メッセージをログに出力
        
        #ラインエディットのテキストを取得
        value = self.ui.lineEdit.text()
        
        check = '^(s:)(.*)$'
        Map = '^(m:)(.*)$'
        
        if not value:
            #入力エリアが未入力の場合「なに？」と表示
            self.ui.labelResponce.setText('なに？')
        elif value == 'm':
            self.rear.Map()
            self.ui.lineEdit.clear()
        elif re.match(Map,value):
            m = self.rear.map_search(value)
            self.ui.labelResponce.setText(m)
            self.ui.lineEdit.clear()
        elif re.match(check,value):
            v = self.rear.search(value)
            self.ui.labelResponce.setText(v)
            self.ui.lineEdit.clear()
        else:
            #インプット文字列を引数にしてdialogue()を実行し、応答メッセージを取得
            response = self.rear.dialogue(value)
            #リアーの応答メッセージをラベルに出力
            self.ui.labelResponce.setText(response)
            
            #プロンプト記号にインプット文字列を連結してログ用のリストに出力
            self.putlog('>' + value)
            
            #リアー専用のプロンプト記号に応答メッセージを連結してログ用のリストに出力
            self.putlog(self.prompt() + response)
            
            #QLineEditクラスのclear()メソッドでラインエディットのテキストをクリア
            self.ui.lineEdit.clear()
        
        self.change_looks()
            
    def closeEvent(self, event):
            #閉じるイベントでコールされるイベントハンドラー
            #ウェジェットを閉じるclose()メソッド実行時にQCloseEventによっと呼ばれる
            
            #オーバーライド
            #メッセージボックスを表示する
            #[Yse]がクリックされたらイベントを続行してウィジェットを閉じる
            #[No]がクリックされたらイベントを取り消してウィジェットを閉じないようにする
            
        reply = QtWidgets.QMessageBox.question(
            self,
            '確認',
            '辞書を更新するよ？',
            buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )#yse|noボタンを表示する
            
        if reply == QtWidgets.QMessageBox.Yes:
            self.rear.save()
            self.writeLog()#対話の一部始終をログファイルに保存
            event.accept()#イベントの続行しcloseする
        else:
            event.ignore()#イベントの取り消し
                
    def showResponderName(self):
            #radioButton_1がオンになった時に呼ばれるイベントハンドラー
            #ラジオボタンの状態を保持するactionの値をTrueにする
            
        self.action = True
            
    def hiddenResponderName(self):
            #2がオンになった時呼ばれるイベントハンドラー
            #action値をFalseにする
            
        self.action = False
            
            
        
        
        
        
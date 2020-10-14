import sys
from PyQt5 import QtWidgets
import mainWindow

#このファイルが直接実行された場合に以下の処理を行う(慣習的)
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)#(sys.argx)--コマンドライン引数を指定
    
    win = mainWindow.MainWindow()#画面を構築するMainWindowクラスのオブジェクトを作成
    win.show()#メインウィンドウを画面に表示
    #メッセージループを開始、プログラムが終了されるまでメッセージループを維持
    #終了時に0が返される
    ret = app.exec_()
    #exec_()の戻り値をシステムに返してプログラムを終了する
    sys.exit(ret)
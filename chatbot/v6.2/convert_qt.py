from PyQt5 import uic


fin = open('qi_rear.ui', 'r', encoding='utf-8')

fout = open('qi_rearUI.py', 'w', encoding='utf-8')

uic.compileUi(fin,fout)

fin.close()
fout.close()


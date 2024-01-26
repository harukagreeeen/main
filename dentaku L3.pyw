# 電卓 Level2

import sys
import tkinter as tk
import math
# メイン関数
def main():
	root = tk.Tk()
	root.title("電卓L2")
	den = Dentaku(root)
	root.mainloop()

# 電卓クラス
class Dentaku():
	# 作成
	def __init__(self, root):
		self.tf = tk.Frame(root)	# トップレベルのフレーム
		self.tf.grid(column = 0, row = 0, padx = 20, pady = 20)

		# ボタンを配置
		ButtonDef = (
		#	 行 列 ラベル 関数
			(4, 0, "0", self.numinput),
			(3, 0, "1", self.numinput),
			(3, 1, "2", self.numinput),
			(3, 2, "3", self.numinput),
			(2, 0, "4", self.numinput),
			(2, 1, "5", self.numinput),
			(2, 2, "6", self.numinput),
			(1, 0, "7", self.numinput),
			(1, 1, "8", self.numinput),
			(1, 2, "9", self.numinput),
			(4, 1, "*", self.mul),
			(4, 2, "/", self.div),
			(1, 3, "-", self.sub),
			(2, 3, "+", self.add),
			(3, 3, "=", self.equal),
			(4, 3, "C", self.clear),
			(5, 0, ".", self.point),
			(5, 1, "d", self.isod),
			(5, 2, "p", self.isop),
			(5, 3, "2進", self.dec2bin))
		root.option_add('*Button.font', 'ＭＳゴシック 28')
		for r, c, label, func in ButtonDef:
			Button = tk.Button(self.tf, text = label)
			Button.bind("<Button-1>", func)
			Button.grid(column = c, row = r, sticky = tk.N +tk.E + tk.S + tk.W)

		# 数字が表示される「エントリー」
		root.option_add('*Entry.font', 'ＭＳゴシック 32')
		self.entVar = tk.StringVar()	# コントロール変数
		self.entVar.set('0')
		self.NumBox = tk.Entry(self.tf, width = 10, textvariable = self.entVar, justify = tk.RIGHT)
		self.NumBox.grid(column = 0, columnspan = 4, row = 0)
		self.初期化()
	# ボタン毎の動作を定義（イベントドライバ群）
	def numinput(self, e):			# 数字キー
		n = int(e.widget["text"])
		if self.小数部 == 1:
			self.n0 = self.n0 * 10 + n
		else:
			self.n0 += self.小数部 * n
			self.小数部 *= 0.1
		self.表示更新()			
	def mul(self, e):				# ×
		self.演算実行()
		self.op = '*' 
	def div(self, e):				# ／
		self.演算実行()
		self.op = '/' 
	def sub(self, e):				# －
		self.演算実行()
		self.op = '-' 
	def add(self, e):				# ＋
		self.演算実行()
		self.op = '+' 
	def equal(self, e):				# ＝
		self.演算実行()
	def clear(self, e):				# Ｃ
		self.n0 = self.n1 = 0
		self.op = ''
		self.entVar.set('0')
		self.小数部 = 1
	def point(self, e):                             # 小数点キー
		self.小数部 = 0.1
	def isod(self, e):	
		aveisod = 0.071
		self.n0 = self.n0 + aveisod
		self.entVar.set('self.n0 + aveisod')
		self.表示更新()
	def isop(self, e):	
		aveisop = 0.130
		self.n0 = self.n0 + aveisop
		self.entVar.set('self.n0 + aveisop')		
		self.表示更新()
	def dec2bin(self, e):		
		self.n0 = format(self.n0, 'b')
		self.entVar.set('self.n0')
		self.表示更新()			
	def 表示更新(self):
		self.entVar.set(str(self.n0))
	def 初期化(self):
		self.n0 = self.n1 = 0
		self.op = ''
		self.小数部 = 1
	def 演算実行(self):
		if self.op == '+':
			self.n0 = self.n1 + self.n0
			self.entVar.set('self.n1 + self.n0')
			self.op = ''
		elif self.op == '-':
			self.n0 = self.n1 - self.n0
			self.entVar.set('self.n1 - self.n0')
			self.op = ''
		elif self.op == '*':
			self.n0 = self.n1 * self.n0
			self.entVar.set('self.n1 * self.n0')
			self.op = ''	
		elif self.op == '/':
			self.n0 = self.n1 / self.n0
			self.entVar.set('self.n1 / self.n0')
			self.op = ''	
		elif self.op == '':
			pass	#　opを調べ、それぞれの計算し、''なら何もしない
		self.表示更新()
		self.n1 = self.n0
		self.n0 = 0
		self.小数部 = 1
if __name__ == '__main__':
	main()

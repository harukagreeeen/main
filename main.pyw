# -*- coding: utf8 -*-
# novel.pyw - ノベルゲームエンジン
# Yo Yamanoguchi
# v.1.0	2018.10.22	HSP版ノベルゲームエンジンから移植

#このコードは、ムーンパワー（ノベルゲーム）のコードに、特定の選択肢を踏むとほかの場面における選択肢を消す機能と、選択肢を増やす機能、ライフの表示を遅らせる機能、ライフを復活して現時点から再開したり最初に戻って初期化などをするリトライ機能を付けた物です

import pygame
from pygame.locals import *
import math
import sys
import pygame.mixer
from button import Button

SFW = 800				# 画面(SURFACE)の幅・高さ
SFH = 600

# 場面クラス
class Scene():
	def __init__(self, imgfile,  message, choice, bgm, life):
		self.image = pygame.image.load( 'シーン画像/' + imgfile)# シーンの画像
		self.frame = pygame.Surface((800, 160))
		self.frame.set_alpha(120)

		self.meslines = message.split(',')					# メッセージ（行分け後）
		self.choice = choice								# 選択肢のリスト
		self.bgm = bgm										# BGM・効果音のファイル
		self.life = life
		self.font = pygame.font.Font("ipag.ttf",20)		# 日本語表示用フォント
		self.lifefont = pygame.font.Font("ipag.ttf", 36)		# 日本語表示用フォント
		self.font.set_bold(True)							# メッセージは太字で表示
								# SceneのIDはScenesリストのインデックスで代用
	# シーンを表示
	def disp(self, SURFACE, life):
		SURFACE.blit(self.image, (0,0))	# シーンの画像を表示
		SURFACE.blit(self.frame, (0,440),)
		for i, line in enumerate(self.meslines):			# メッセージを行毎に表示
			mesimage = self.font.render(line, True, (170, 170, 170),)#170
			SURFACE.blit(mesimage, (8, 470 + i * 24))


		if life != None:
			life += self.life
			lifeimage = self.lifefont.render("life: {}".format(life), True, (255, 102, 153))
		else:
			lifeimage = self.lifefont.render("", True, (255, 102, 153))



		SURFACE.blit(lifeimage, (40, 30))
		if len(self.bgm):									# BGM・効果音を再生
			pygame.mixer.music.load('BGM/' + self.bgm)
			pygame.mixer.music.play()
		cb = list()											# 選択肢からボタンを作成
		cl = len(self.choice)								# 選択肢の数
		for i, cc in enumerate(self.choice):
			x = (SFW - cl * 120) / 2 + (120 * i)	# ボタン位置 x120
			y = SFH - 55								# ボタン位置
			cb.append(Button())
			cb[i].create(SURFACE, x, y, 0, 50, 110, cc[0], bg = (0,0,0))#ここの50/120を変更すれば、選択肢変更可能
		while True:											# イベント取得待ち
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:				# 画面右上の終了ボタン
					pygame.quit()
				elif event.type == MOUSEBUTTONDOWN:			# マウスボタンのクリック
					for i, bt in enumerate(cb):				# 各選択肢をチェック
						if bt.pressed(pygame.mouse.get_pos()):
							print("button[{}] pressed.".format(i))
							return self.choice[i][1],life		# 次に表示されるScene番号を返す
					
				elif event.type == MOUSEBUTTONDOWN:			# マウスボタンのクリック
					for i, bt in enumerate(cb):				# 各選択肢をチェック
						if bt.pressed(pygame.mouse.get_pos()):
							print("button[{}] pressed.".format(i))
							return self.choice[i][1],life		# 次に表示されScene番号を返す

# ゲーム実行
def main():
	sceneNo = 0					# シナリオファイル読み込み前のシーンNo.
	Scenes = list()				# 全シーンのリスト

	pygame.init()
	SURFACE = pygame.display.set_mode((SFW, SFH))

	# シナリオファイルを読んで各Sceneに展開、Scenesリストに格納
	with open('テキスト.txt', 'r') as sf:
		while True:
			line = sf.readline()	# シーン番号は読み飛ばす
			if not line:			# シナリオファイルの[EOF]
				break;
			imgfile = sf.readline().rstrip("\n")	# 改行コードを削除
			message = sf.readline().rstrip("\n")
			choicestr = sf.readline().rstrip("\n")	# 選択肢行から選択肢リストを作成
			choice = list()
			if len(choicestr):
				tmpcl = choicestr.split(',')
				it = iter(tmpcl)					# リストの要素を2つ1組で処理する
				for label, jump in zip(it, it):
					choice.append([label, int(jump)])	# 選択肢リストはリストのリスト
			else:
				choice.append(['▼', sceneNo + 1])	# 選択肢行がないときの処理
			bgm = sf.readline().rstrip("\n")
			lifestr = sf.readline().rstrip("\n")

			if lifestr:
				life = int(lifestr)
			else:
				life = 0

			scene = Scene(imgfile, message, choice, bgm, life)	# Sceneオブジェクトを作成
			

		
			Scenes.append(scene)	# Scenesリストに追加
			sceneNo += 1			# シーンNo.をインクリメント
							# シナリオファイルは自動的にcloseする（with関数）


	#特定のチョイスの削除　関数
	def elim(trap, now, word):
		if scene == trap:
			for cho in Scenes[now].choice:
				if cho[0] == word:
					Scenes[now].choice.remove(cho)


	#初期化における削除　関数
	def elmnit(now, word):
		if scene == 0 or scene == 42:
			for cho in Scenes[now].choice:
				if cho[0] == word:
					Scenes[now].choice.remove(cho)


	#特定のチョイスの追加　関数
	def add(trap, now, word, jump):
		if scene == trap:
			Scenes[now].choice.append([word, int(jump)])
		

	#初期化における追加　関数
	def adnit(now, word, jump):
		if scene == 0 or scene == 42: 
			Scenes[now].choice.append([word, int(jump)])
			

	# プレイ開始
	scene = 0					# ゲームスタート時のシーンNo.
	life = None
	  #答え表示分岐
	while True:
		scene,life = Scenes[scene].disp(SURFACE,life)	# そのシーンを表示
		print(scene)


	# 特定の選択肢を踏んだ時、特定のチョイスが消される
		

		elim(1,154,"仮置き")

		#聞き込みの選択肢変化

		elim(60,59,"宇和佐")
		elim(71,60,"昨日と今日の行動")
		elim(79,60,"一路の指示")
		elim(88,80,"昨日と今日の行動")
		elim(66,83,"聞けることはもうない")
		elim(90,89,"昨日と今日の行動")
		elim(97,89,"付き合っている噂") 


		#聞き込みを二人で終わらせるためのもの

		elim(326,327,"宇和佐")
		elim(326,327,"次席")
		elim(327,328,"宇和佐")
		elim(327,328,"森澄")
		elim(328,326,"次席")
		elim(328,326,"森澄")
		elim(328,327,"宇和佐")
		elim(328,327,"次席")
		elim(326,328,"宇和佐")
		elim(326,328,"森澄")
		elim(327,326,"次席")
		elim(327,326,"森澄") 


		#証拠をそろえるところ

		elim(103,102,"黒板")
		elim(108,102,"ロッカー")
		elim(113,102,"メダカ水槽")
		elim(119,118,"落ちている紙")
		elim(123,118,"絵が置いてあった場所")
		elim(127,118,"焼却炉")


		#第一犯人

		elim(138,137,"宇和佐")
		elim(139,137,"次席")
		elim(140,137,"一路")
		

		#森澄供述

		elim(150,149,"異議あり")
		elim(329,151,"異議あり")
		elim(330,152,"次へ")
		elim(122,154,"ない")
		elim(160,154,"ない")


		#第二犯人

		elim(186,185,"宇和佐")
		elim(187,185,"一路")
		

		#次席供述

		elim(199,198,"異議あり")
		elim(331,200,"異議あり")
		elim(332,201,"次へ")


		#出会ってしまった人物

		elim(266,265,"一路")
		elim(266,265,"次席")
		
		
		#再挑戦用の選択肢
		elim(152,324,"諦めない")
		elim(154,324,"諦めない")
		elim(185,324,"諦めない")
		elim(198,324,"諦めない")
		elim(200,324,"諦めない")
		elim(201,324,"諦めない")
		elim(208,324,"諦めない")
		elim(220,324,"諦めない")
		elim(233,324,"諦めない")
		elim(245,324,"諦めない")
		elim(265,324,"諦めない")
		elim(277,324,"諦めない")
		elim(282,324,"諦めない")
		

	# 特定の選択肢を踏んだ時、特定のチョイスが消される　


		#単発で加えないといけない物

		add(66, 83, "校長室の件について",84)
		add(66, 89, "付き合っている噂",97) 	
		add(122, 154, "ある",161) 
		add(160, 154, "ある",161)


		#聞き込みを二人で終わらせるためのもの

		add(326,327,"聞き込みを終える",100)
		add(326,328,"聞き込みを終える",100)
		add(327,328,"聞き込みを終える",100)
		add(327,326,"聞き込みを終える",100)
		add(328,327,"聞き込みを終える",100)
		add(328,326,"聞き込みを終える",100)

		
		#なくなった鍵、の選択肢

		add(175,220,"なくなった鍵",224)
		add(71,220,"次席と森澄の噂",221)
		add(107,220,"新品の手袋",221)
		

		#宇和佐のメモの選択肢

		add(112,245,"新聞紙",246)
		add(79,245,"宇和佐のメモ",249)
		add(107,245,"今週の当番",246)
		

		#ラス問　絵の痕跡

		add(126,277,"パレット",278)
		add(131,277,"焼却炉のロック",278)
		add(126,277,"絵の痕跡",281)
		
		#ラス問　黄色く濁った水槽の水

		add(107,282,"新品の手袋",283)
		add(131,282,"焼却炉のロック",283)
		add(116,282,"黄色く濁った水槽の水",287)
		

		#再挑戦用の選択肢

		add(346,324,"諦めない",325)
		add(348,324,"諦めない",333)
		add(156,324,"諦めない",334)
		add(190,324,"諦めない",335)
		add(350,324,"諦めない",336)
		add(352,324,"諦めない",337)
		add(354,324,"諦めない",338)
		add(214,324,"諦めない",339)
		add(223,324,"諦めない",340)
		add(236,324,"諦めない",341)
		add(248,324,"諦めない",342)
		add(356,324,"諦めない",343)
		add(358,324,"諦めない",344,)
		add(286,324,"諦めない",345,)



#ここからは、初期化に関する削除と追加(再挑戦用）(999を経由しない場合)

		
	#初期化するときに、まず前回加えたものを戻す

	
		#単発で加えないといけない物

		elmnit(83, "校長室の件について")
		elmnit(89, "付き合っている噂") 	
		elmnit(154, "ある") 


		#聞き込みを二人で終わらせるためのもの

		elmnit(327,"聞き込みを終える")
		elmnit(328,"聞き込みを終える")
		elmnit(328,"聞き込みを終える")
		elmnit(326,"聞き込みを終える")
		elmnit(327,"聞き込みを終える")
		elmnit(326,"聞き込みを終える")

		
		#なくなった鍵、の選択肢

		elmnit(220,"なくなった鍵")
		elmnit(220,"次席と森澄の噂")
		elmnit(220,"新品の手袋")
		

		#宇和佐のメモの選択肢

		elmnit(245,"新聞紙")
		elmnit(245,"宇和佐のメモ")
		elmnit(220,"今週の当番")
		

		#ラス問　絵の痕跡

		elmnit(277,"パレット")
		elmnit(277,"焼却炉のロック")
		elmnit(227,"絵の痕跡")
		
		#ラス問　黄色く濁った水槽の水

		elmnit(282,"新品の手袋")
		elmnit(282,"焼却炉のロック")
		elmnit(282,"黄色く濁った水槽の水")
		

	#初期化するときに、いったん前に消さなかった物も消す


		#聞き込みの選択肢変化

		elmnit(59,"宇和佐")
		elmnit(59,"森澄")
		elmnit(59,"次席")
		elmnit(60,"昨日と今日の行動")
		elmnit(60,"一路の指示")
		elmnit(80,"昨日と今日の行動")
		elmnit(83,"聞けることはもうない")
		elmnit(89,"昨日と今日の行動")
		elmnit(89,"付き合っている噂") 


		#聞き込みを二人で終わらせるためのもの

		elmnit(327,"宇和佐")
		elmnit(327,"次席")
		elmnit(328,"宇和佐")
		elmnit(328,"森澄")
		elmnit(326,"次席")
		elmnit(326,"森澄")
		

		#証拠をそろえるところ

		elmnit(102,"黒板")
		elmnit(102,"ロッカー")
		elmnit(102,"メダカ水槽")
		elmnit(118,"落ちている紙")
		elmnit(118,"絵が置いてあった場所")
		elmnit(118,"焼却炉")


		#第一犯人

		elmnit(137,"宇和佐")
		elmnit(137,"次席")
		elmnit(137,"一路")
		

		#森澄供述

		elmnit(149,"異議あり")
		elmnit(151,"異議あり")
		elmnit(152,"異議あり")#順番揃えるため
		elmnit(152,"次へ")
		elmnit(154,"ない")


		#第二犯人

		elmnit(185,"宇和佐")
		elmnit(185,"一路")
		

		#次席供述

		elmnit(198,"異議あり")
		elmnit(200,"異議あり")
		elmnit(201,"次へ")
		elmnit(201,"異議あり")

		#出会ってしまった人物

		elmnit(265,"一路")
		elmnit(265,"次席")
		
		
		elmnit(324,"諦めない")


	#初期化するときに、初めからあった物だけを元に戻す


		#聞き込みの選択肢変化 ※あとから増えるものはaddしない

		adnit(59,"宇和佐",60)
		adnit(59,"森澄",80)
		adnit(59,"次席",89)
		adnit(60,"昨日と今日の行動",61)
		adnit(60,"一路の指示",73)
		adnit(80,"昨日と今日の行動",81)
		adnit(83,"聞けることはもうない",327)
		adnit(89,"昨日と今日の行動",90)


		#聞き込みを二人で終わらせるためのもの

		adnit(327,"宇和佐",60)
		adnit(327,"次席",89)
		adnit(328,"宇和佐",60)
		adnit(328,"森澄",80)
		adnit(326,"森澄",80)
		adnit(326,"次席",89)

		#証拠をそろえるところ

		adnit(102,"黒板",103)
		adnit(102,"ロッカー",108)
		adnit(102,"メダカ水槽",113)
		adnit(118,"落ちている紙",119)
		adnit(118,"絵が置いてあった場所",123)
		adnit(118,"焼却炉",127)


		#第一犯人

		adnit(137,"宇和佐",138)
		adnit(137,"次席",139)
		adnit(137,"一路",140)
		

		#森澄供述

		adnit(149,"異議あり",150)
		adnit(151,"異議あり",329)
		adnit(152,"次へ",330)
		adnit(152,"異議あり",153)
		adnit(154,"ない",155)


		#第二犯人

		adnit(185,"宇和佐",186)
		adnit(185,"一路",187)
		

		#次席供述

		adnit(198,"異議あり",199)
		adnit(200,"異議あり",331)
		adnit(201,"次へ",332)
		adnit(201,"異議あり",202)

		#出会ってしまった人物

		adnit(265,"一路",266)
		adnit(265,"次席",266)
		
		
	#ライフの処理


		if scene == 0:  #lifeの初期化
			life = None
			
		if scene == 136:
			life = 5

		if scene == 346 and life == 0:
			scene = 323
		if scene == 348 and life == 0:
			scene = 323
		if scene == 156 and life == 0:
			scene = 323
		if scene == 190 and life == 0:
			scene = 323
		if scene == 350 and life == 0:
			scene = 323
		if scene == 352 and life == 0:
			scene = 323
		if scene == 354 and life == 0:
			scene = 323
		if scene == 214 and life == 0:
			scene = 323
		if scene == 223 and life == 0:
			scene = 323
		if scene == 236 and life == 0:
			scene = 323	
		if scene == 248 and life == 0:
			scene = 323
		if scene == 356 and life == 0:
			scene = 323
		if scene == 358 and life == 0:
			scene = 323	
		if scene == 286 and life == 0:
			scene = 323	
		
		if scene == 999:		# シーンNo.が「999」なら終了
			break				# ゲーム終了

if __name__ == "__main__":
	main()


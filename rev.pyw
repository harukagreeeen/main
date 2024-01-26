# -*- coding: utf8 -*-
# novel.pyw - ノベルゲームエンジン
# Yo Yamanoguchi
# v.1.0	2018.10.22	HSP版ノベルゲームエンジンから移植

import pygame
from pygame.locals import *
import math
import sys
import pygame.mixer
from button import Button

SFW = 800						# 画面(SURFACE)の幅・高さ
SFH = 600

# 場面クラス
class Scene():
	def __init__(self, imgfile,  message, choice, bgm, life):
		self.image = pygame.image.load('シーン画像/' + imgfile)	# シーンの画像
		self.frame = pygame.Surface((800, 160))
		self.frame.set_alpha(120)

		self.meslines = message.split(',')					# メッセージ（行分け後）
		self.choice = choice								# 選択肢のリスト
		self.bgm = bgm										# BGM・効果音のファイル
		self.font = pygame.font.Font("ipag.ttf",20)		# 日本語表示用フォント
			# 日本語表示用フォント
		self.font.set_bold(True)							# メッセージは太字で表示
								# SceneのIDはScenesリストのインデックスで代用
	# シーンを表示
	def disp(self, SURFACE, life):
		SURFACE.blit(self.image, (0,0))	# シーンの画像を表示
		SURFACE.blit(self.frame, (0,440),)
		for i, line in enumerate(self.meslines):			# メッセージを行毎に表示
			mesimage = self.font.render(line, True, (170, 170, 170),)
			SURFACE.blit(mesimage, (8, 470 + i * 24))

		

	
		if len(self.bgm):									# BGM・効果音を再生
			pygame.mixer.music.load('BGM/' + self.bgm)
			pygame.mixer.music.play()
		cb = list()											# 選択肢からボタンを作成
		cl = len(self.choice)								# 選択肢の数
		for i, cc in enumerate(self.choice):
			x = (SFW - cl * 120) / 2 + (120 * i)	# ボタン位置 x
			y = SFH - 50								# ボタン位置
			cb.append(Button())
			cb[i].create(SURFACE, x, y, 0, 40, 80, cc[0], bg = (0,0,0))
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
	# プレイ開始
	scene = 0					# ゲームスタート時のシーンNo.
	
	pygame.quit()				# ゲーム終了

if __name__ == "__main__":
	main()


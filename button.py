# -*- coding: utf8 -*-
# button.py - pygame用Buttonクラス
# Yo.Yamanoguchi


import pygame
from pygame.locals import *

# Buttonクラス
class Button:
	# 表示               位置  サイズ   ラベル 文字色              背景色
	def create(self, sf, x, y, w, h, l, text, fg = (255, 255, 255), bg = (0, 0, 0)):
		self.fg = fg			# 文字色
		self.bg = bg			# 背景色
		sf = self.draw_button(sf, x, y, w, h, l)	# ボタン面を描画
		sf = self.write_text(sf, x, y, w, h, l, text)	# ラベルを書く
		self.rect = pygame.Rect(x, y, l, h)	# 範囲を保存（push判定用）
		return sf

	# ラベルを書く
	def write_text(self, sf, x, y, w, h, l, text):
		font_size = int(l // (len(text) + 1))	# ラベルの文字数からフォントサイズを計算
		myFont = pygame.font.Font("ipag.ttf", font_size)	# 日本語表示用IPAフォント
		myText = myFont.render(text, 1, self.fg)	# ラベル画像を作成・ゲーム画面に貼り付け
		sf.blit(myText, ((x + l / 2) - myText.get_width() / 2, (y + h / 2) - myText.get_height() / 2))
		return sf

	# ボタン面を描画
	def draw_button(self, sf, x, y, w, h, l):		   
		for i in range(1, 10):	# 透明度を変えながら外枠を描く（フェードアウト風）
			s = pygame.Surface((l + (i * 2), h + (i * 2)))
			s.fill(self.bg)
			alpha = (255 / (i + 2))
			if alpha <= 0:
				alpha = 1
			s.set_alpha(alpha)
			pygame.draw.rect(s, self.fg, (x - i, y - i, l + i, h + i), w)
			sf.blit(s, (x - i, y - i))
		pygame.draw.rect(sf, self.bg, (x, y, l, h), 0)	# ボタン面
		pygame.draw.rect(sf, (190,190,190), (x, y, l, h), 1)	# 細線で装飾
		return sf

	# ボタンが押されたかどうか判定
	def pressed(self, mpos):	# pygameの衝突判定機能を利用
		return self.rect.collidepoint(mpos)

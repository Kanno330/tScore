import pokeLoadDeckCode
import json
import ui
import clipboard
import checkStartPokemon

class SeedListTableView(object):
	def __init__(self):
		# デッキコード取得
		code = clipboard.get()
		# デッキデータ取得
		self.deck = pokeLoadDeckCode.pokeLoadDeckCode(code)
		# たねポケモンリスト
		self.seedList = []
		for id in self.deck.keys():
			if self.deck[id].get('evol') == 'たね':
				self.seedList.append(
					{
						'title':self.deck[id].get('nameAlt')
						, 'id':id
					}
				)
		# データセット作成
		self.ds = ui.ListDataSource('')
		self.ds.items = self.seedList
		self.ds.move_enabled = True
		self.ds.delete_enabled = False
		# テーブル作成
		self.tv = ui.TableView()
		self.tv.name = 'Seed List'
		self.tv.delegate = self
		self.tv.data_source = self.ds
		self.tv.editing = True
		# ボタン作成
		self.bi = ui.ButtonItem(title='Check!')
		self.bi.action = self.checkStartPokemon
		# 画面作成
		self.nv = ui.NavigationView(self.tv)
		self.nv.name = 'Pokemon Start Card Check'
		self.nv.right_button_items = [self.bi]

	def checkStartPokemon(self, sender):
		print('優先度')
		for i, seed in enumerate(self.ds.items):
			print(self.deck[seed.get('id')].get('nameAlt'))
			self.deck[seed.get('id')]['priority'] = int(60 - i)
		else:
			print('')

		code = clipboard.get()
		loop = 125000

		with open('deckInfo/' + code + '.json', 'w', encoding='utf-8') as f:
		json.dump(self.deck, f, indent=4, ensure_ascii=False)

		checkStartPokemon.checkStartPokemon(code, loop)

		self.nv.close()

def main():
	# code = 'fkV5FV-bg5uX5-fvwVVk'
	sltv = SeedListTableView()
	sltv.nv.present('sheet')

if _name_ == '__main__':
	main()

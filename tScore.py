import ui

class tScoreView(object):
	def __init__(self):
		# 画面サイズ(iPhone 6 ~ iPhone XS)
		# XR, XSMaxは(414, 896)
		self.view = ui.View(0, 0, 375, 667)
		self.view.name = 'tScore'
		self.view.background_color = 'white'

		# ラベルの追加
		self.label = ui.Label(frame=(0, 0, self.view.width, 30))
		self.label.background_color = (0, 0, 0, 0.5)
		self.label.text_color = 'white'
		self.label.alignment = ui.ALIGN_CENTER
		self.label.text = 'test_label!!' 
		self.view.add_subview(self.label)

		# ボタンの追加
		self.button = ui.Button(title='Tap me!')
		self.button.center = (self.view.width * 0.5, self.view.height * 0.5)
		self.button.flex = 'LRTB'
		self.button.action = self.button_tapped
		self.view.add_subview(self.button)
		
		self.button2 = ui.Button()
		self.button2.frame = (10, 100, self.view.width-20, 30)
		self.button2.title = 'test_button'
		self.button2.action = self.button_tapped
		self.button2.background_color = (0, 0, 0, 0.5)
		self.button2.tint_color = ('white')
		self.view.add_subview(self.button2)
	
	def button_tapped(self, sender):
		sender.title = 'Hello'

def main():
	v = tScoreView()
	v.view.present(style='sheet', hide_title_bar='True')

if __name__ == '__main__':
	main()

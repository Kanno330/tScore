import ui

class tScoreView(object):
	def __init__(self):
		self.view = ui.View()
		self.view.name = 'tScore'
		self.view.background_color = 'white'
		self.button = ui.Button(title='Tap me!')
		self.button.center = (view.width * 0.5, view.height * 0.5)
		self.button.flex = 'LRTB'
		self.button.action = button_tapped
		self.view.add_subview(button)
	
	def button_tapped(self, sender):
		sender.title = 'Hello'

def main():
	v = tScoreView()
	v.view.present('sheet')

if __name__ == '__main__':
	main()

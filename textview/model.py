from prettytable import PrettyTable as pt
from texttable import Texttable

class TextViewModel:
	"""
	Класс для отображения данных в виде таблицы
	"""
	def __init__(self, config):
		self.config = config

	def waiting_command(self):
		return "Ожидание ввода команды ..."



from flask import jsonify
from ajax.product_list import ProductList

class ManagerRequest():
	def __init__(self, path):
		self.path = path

	def _validate_sub(self, s:str) -> bool:
		if s in self.path: return True
		return False

	def get_last_value(self) -> str:
		value = self.path.split("_")[-1]
		return value
	
	def is_command_click_bot(self) -> bool:
		return self._validate_sub("click")

	def is_command_update_page(self) -> bool:
		return self._validate_sub("update")

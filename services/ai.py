from openai import OpenAI


GROUP_LITERATURA = 'литература и афоризмы'
GROUP_WORKS = 'обьявления о работе'
GROUP_NEWS = 'новости и события'

TYPES_GROUPS = [GROUP_LITERATURA,GROUP_WORKS,GROUP_NEWS]

class Ai():
	def __init__(self, config):
		self.api_base = config.get_deepseek_api_base()
		self.api_key = config.get_deepseek_api_key()
		self.symbol_split = "symbol_split_here"		
		
		self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)

	def get_formatted_post_works(self, data:str) -> list[str]:
		pre_promt = f"не добавляя комментариев по сделанной работе выполни задание, не добавляя от себя текста и предложений: отформатируй для красивого поста в телеграмм-группу о работе, используй смайлы, а ссылки и контакты оформи знаками || вначале и в конце, а до объявлений,между объявлениями и после них - добавляй для разделения {self.symbol_split}"
		response = self.client.chat.completions.create(
			model="deepseek-chat", 
			messages=[
				{"role": "system", "content": "You are a helpful assistant"},
				{"role": "user", "content":f"{pre_promt} {data}"},
			],
			stream = False 
		)
		res = response.choices[0].message.content
		res = res.split(self.symbol_split)
		return res
	
	def get_formatted_post_libraries(self, data:str) -> list[str]:
		pre_promt = f"не добавляя комментариев по сделанной работе выполни задание, не добавляя от себя текста и предложений: подготовь для поста в телеграмм-группу с цитатами и афоризмами: исправь смайлы и знаки форматирования, ссылки и контакты с предложением подписаться и подобное - удали, а до объявлений, между объявлениями и после них - добавляй для разделения {self.symbol_split}, а также удали те блоки в которых есть реклама"
		response = self.client.chat.completions.create(
			model="deepseek-chat",
			messages=[
				{"role": "system", "content": "You are a helpful assistant"}, 
				{"role": "user", "content":f"{pre_promt} {data}"},
			],
			stream = False 
		)
		res = response.choices[0].message.content
		res = res.split(self.symbol_split)
		return res
	
	def get_formatted_post_news(self, data:str) -> list[str]:
		pre_promt = f"не добавляя комментариев по сделанной работе выполни задание, не добавляя от себя текста и предложений: отформатируй для поста в телеграмм-группу новостей, используй смайлы, а ссылки и контакты оформи знаками || вначале и в конце, а до объявлений,между объявлениями и после них - добавляй для разделения {self.symbol_split}"
		response = self.client.chat.completions.create(
			model="deepseek-chat", 
			messages=[
				{"role": "system", "content": "You are a helpful assistant"},
				{"role": "user", "content":f"{pre_promt} {data}"},
			],
			stream = False 
		)
		res = response.choices[0].message.content
		res = res.split(self.symbol_split)
		return res
	
	def automatic_formatted_message(self, message):
		pre_promt = f"определи к какой группе относятся сообщения из перечисленных: {TYPES_GROUPS}. напиши в ответе только название соответствующей категории и больше ничего. не добавляй в ответ комментариев и разъяснений - тольео название категориии"
		response = self.client.chat.completions.create(
			model="deepseek-chat", 
			messages=[
				{"role": "system", "content": "You are a helpful assistant"},
				{"role": "user", "content":f"{pre_promt} {message}"},
			],
			stream = False 
		)
		res = response.choices[0].message.content
		
		temp_text = "pass"

		if res in TYPES_GROUPS:
			if res == GROUP_LITERATURA:
				temp_text = self.get_formatted_post_libraries(message.text)
			elif res == GROUP_WORKS:
				temp_text = self.get_formatted_post_works(message.text)
			elif res == GROUP_NEWS:
				temp_text = self.get_formatted_post_news(message.text)
		print(temp_text, res)
		return temp_text

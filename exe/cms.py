import textwrap
import arcade

from arcade.gui import (
	UIAnchorLayout,
	UIBoxLayout,
	UIButtonRow,
	UIFlatButton,
	UIImage,
	UILabel,
	UIManager,
	UIMessageBox,
	UIOnActionEvent,
	UISpace,
	UITextArea,
	UIView,
)

arcade.resources.load_kenney_fonts()

DEFAULT_FONT = ("Kenney Future", "arial")
DETAILS_FONT = ("arial", "Kenney Future Narrow")

TEXTURE_LOGO_CMS = arcade.load_texture("images/logo_cms.jpg")

class GalleryView(UIView):
	def __init__(self):
		super().__init__()
		self.background_color = arcade.uicolor.BLUE_BELIZE_HOLE

		root = self.add_widget(UIAnchorLayout())

		# Setup side navigation
		nav_side = UIButtonRow(vertical=True, size_hint=(0.2, 1))
		nav_side.add(
			UILabel(
				"Навигация",
				font_name=DEFAULT_FONT,
				font_size=32,
				text_color=arcade.uicolor.DARK_BLUE_MIDNIGHT_BLUE,
				size_hint=(1, 0.1),
				align="center",
			)
		)
		nav_side.add(UISpace(size_hint=(1, 0.01), color=arcade.uicolor.DARK_BLUE_MIDNIGHT_BLUE))

		nav_side.with_padding(all=10)
		nav_side.with_background(color=arcade.uicolor.WHITE_CLOUDS)
		nav_side.add_button("🌐 О платформе", style=UIFlatButton.DEFAULT_STYLE, size_hint=(2, 0.1))
		nav_side.add_button("💼 Возможности", style=UIFlatButton.DEFAULT_STYLE, size_hint=(1, 0.1))
		nav_side.add_button("📱 Демонстрация", style=UIFlatButton.DEFAULT_STYLE, size_hint=(1, 0.1))
		nav_side.add_button("✅ Получить", style=UIFlatButton.DEFAULT_STYLE, size_hint=(1, 0.1))
		root.add(nav_side, anchor_x="left", anchor_y="top")

		@nav_side.event("on_action")
		def on_action(event: UIOnActionEvent):
			if event.action == "🌐 О платформе":
				self._show_about_platform()
			elif event.action == "💼 Возможности":
				self._show_targets()
			elif event.action == "📱 Демонстрация":
				self._show_demo()
			elif event.action == "✅ Получить":
				self._show_getting()
			# elif event.action == "Other":
			# 	self._show_other_widgets()

		# Setup content to show widgets in

		self._body = UIAnchorLayout(size_hint=(0.8, 1))
		self._body.with_padding(all=20)
		root.add(self._body, anchor_x="right", anchor_y="top")

		# init start widgets
		self._show_about_platform()


	def _show_targets(self):
		self._body.clear()

		self._body.add(UILabel(
			text="Возможности 💡", 
			size_hint=(0.1, 0.1),
			font_name=DETAILS_FONT,
			font_size=25,
		),
		anchor_y="top")

		self._body.add(UISpace(size_hint=(0.2, 0.1)))
		text_area = self._body.add(
			UITextArea(
				text=textwrap.dedent("""			
						 Платформа предлагает широкий спектр возможностей, которые помогают вам достигать поставленных целей:
						 
						 1. Автопостинг: Настройте автоматическую публикацию контента из различных источников, включая Telegram-каналы и веб-ресурсы. Это позволяет вам сосредоточиться на создании качественного контента.

						 2. Управление ботами: Удобный интерфейс управления позволяет вам быстро и легко настраивать всех ботов из одного места, контролируя их функции и параметры.
						 
						 3. Аналитика: Получайте информацию о взаимодействии с вашим контентом. Вы можете отслеживать, какие сообщения вызывают наибольшую реакцию и где нужно улучшить свою стратегию.
						 
						 4. Глобальные настройки: Настройте такие параметры, как тайм-аут между сообщениями, права доступа для администраторов и многое другое, чтобы контролировать вашу экосистему.
						 
						 5. Сообщество единомышленников: Присоединяйтесь к другим пользователям, делитесь опытом и находите вдохновение для новых идей.
			""").strip(),
				font_name=DETAILS_FONT,
				font_size=16,
				text_color=arcade.uicolor.WHITE,
				size_hint=(1, 0.7),
			),
			anchor_y = "center",
		)
		text_area.with_padding(left=10, right=10)
		text_area.with_border(color=arcade.uicolor.GRAY_CONCRETE, width=2)


		next_page = self._body.add(
			UIFlatButton(
				text="Далее", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="right",
			align_y=20,
		)
		prev_page = self._body.add(
			UIFlatButton(
				text="Назад", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="left",
			align_y=20,
		)

		@next_page.event("on_click")
		def on_click(_):
			self._show_demo()
		
		@prev_page.event("on_click")
		def on_click(_):
			self._show_about_platform()


	def _show_about_platform(self):
		self._body.clear()
		
		self._body.add(UILabel(
			text="О платформе 🌐", 
			size_hint=(0.1, 0.1),
			font_name=DETAILS_FONT,
			font_size=25,
		),
		anchor_y="top")

		self._body.add(UISpace(size_hint=(0.2, 0.1)))
		text_area = self._body.add(
			UITextArea(
				text=textwrap.dedent("""
				Наша платформа представляет собой уникальную экосистему, 
				где вы можете легко объединять группы, каналы и сообщества.
						 

				Мы разработали пространство, которое не только облегчает процесс управления контентом, 
				но и помогает развивать ваше сообщество, устанавливать связи и делиться ценным информацией. 
						 
				Наша цель — сделать общение более эффективным и увлекательным для всех пользователей.
						 
				Экосистема включает в себя мощные инструменты для автоматизации, 
				такие как боты для автопостинга, которые работают круглосуточно, 
				обеспечивая актуальность и свежесть вашего контента. 
						 
				Используя различные источники, вы получаете возможность 
				создавать качественный контент, 
				способствующий росту и вовлечению подписчиков.
						 
				Youtube Demo Video: https://youtu.be/sjuay5Rix1w?si=t37Guln_QWJXqiBF
						 
			""").strip(),
				font_name=DETAILS_FONT,
				font_size=16,
				text_color=arcade.uicolor.WHITE,
				size_hint=(1, 0.7),
			),
			anchor_y = "center",
		)
		text_area.with_padding(left=10, right=10)
		text_area.with_border(color=arcade.uicolor.GRAY_CONCRETE, width=2)

		next_page = self._body.add(
			UIFlatButton(
				text="Далее", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="right",
			align_y=20,
		)
		prev_page = self._body.add(
			UIFlatButton(
				text="Назад", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="left",
			align_y=20,
		)

		@next_page.event("on_click")
		def on_click(_):
			self._show_targets()
		
		@prev_page.event("on_click")
		def on_click(_):
			self._show_getting()


	def _show_demo(self):
		self._body.clear()
		
		box = UIBoxLayout(vertical=True, size_hint=(1, 1), align="left", space_between=5)
	

		self._body.add(box)
		self._body.add(UISpace(size_hint=(0.2, 0.1)))

		next_page = self._body.add(
			UIFlatButton(
				text="Далее", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="right",
			align_y=20,
		)
		prev_page = self._body.add(
			UIFlatButton(
				text="Назад", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="left",
			align_y=20,
		)

		@next_page.event("on_click")
		def on_click(_):
			self._show_getting()
		
		@prev_page.event("on_click")
		def on_click(_):
			self._show_targets()



	def _show_getting(self):
		self._body.clear()

		self._body.add(UILabel(
			text="Получить ✅", 
			size_hint=(0.1, 0.1),
			font_name=DETAILS_FONT,
			font_size=25,
		),
		anchor_y="top")
		

		self._body.add(UISpace(size_hint=(0.2, 0.1)))
		text_area = self._body.add(
			UITextArea(
				text=textwrap.dedent("""
Мы понимаем, что у вас могут возникнуть вопросы или потребности в поддержке во время работы с нашей платформой. Наша команда поддержки предоставляет разнообразные каналы для помощи:

- Часто задаваемые вопросы (FAQ): Мы собрали список ответов на самые популярные вопросы, чтобы вы могли быстро найти необходимую информацию.
- Техническая поддержка: Наши эксперты готовы помочь вам справиться с любыми техническими проблемами через [форму обратной связи]().
- Вебинары и обучающие материалы: Присоединяйтесь к нашим онлайн-сессиям, где мы обучаем пользователей новым функциям и стратегиям на платформе. Смотрите расписание на странице [обучения](#).

Мы здесь, чтобы помочь вам получить максимальную выгоду от нашей экосистемы и достичь ваших целей! 💪
						 
Youtube Demo Video: https://youtu.be/sjuay5Rix1w?si=t37Guln_QWJXqiBF
			""").strip(),
				font_name=DETAILS_FONT,
				font_size=16,
				text_color=arcade.uicolor.WHITE,
				size_hint=(1, 0.7),
			),
			anchor_y = "center",
		)
		text_area.with_padding(left=10, right=10)
		text_area.with_border(color=arcade.uicolor.GRAY_CONCRETE, width=2)

		next_page = self._body.add(
			UIFlatButton(
				text="Далее", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="right",
			align_y=20,
		)

		mid_page = self._body.add(
			UIFlatButton(
				text="Получить", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="center",
			align_y=20,
		)

		prev_page = self._body.add(
			UIFlatButton(
				text="назад", style=UIFlatButton.DEFAULT_STYLE, size_hint=(0.3, 0.1)
			),
			anchor_y="bottom",
			anchor_x="left",
			align_y=20,
		)

		@next_page.event("on_click")
		def on_click(_):
			self._show_about_platform()
		
		@mid_page.event("on_click")
		def on_click(_):
			self.ui.add(
				UIMessageBox(
					width=500,
					height=150,
					title="Свяжитесь с нами!",
					buttons=("Ок","Закрыть"),
					message_text=textwrap.dedent("""
					Через почту: yuran.ignatenko@yandex.ru
					Telegram: https://t.me/Dartanyans
					""").strip(),
				),
				layer=UIManager.OVERLAY_LAYER,
			)

		@prev_page.event("on_click")
		def on_click(_):
			self._show_demo()



def main():
	window = arcade.Window(title="GUI Example: Widget Gallery")
	window.show_view(GalleryView())
	window.run()


if __name__ == "__main__":
	main()
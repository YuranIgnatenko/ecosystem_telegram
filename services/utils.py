from PIL import Image

TYPE_SERVICE_TELEGRAM_SCRAPPER = "telegram_scrapper"
TYPE_SERVICE_WEB_PARSER = "web_parser"
SIZE_MB_20 = 20 * 1024 * 1024

def resize_image(file: str, coefficient: float = 0.7):
	with Image.open(file) as image:
		resized = image.resize((int(image.width * coefficient), int(image.height * coefficient)))
		resized.save(file)


def compress_image(file: str, quality: int = 70):
	with Image.open(file) as image:
		while quality > 0:
			image.save(file, optimize=True, quality=quality, format="JPEG")
			quality -= 5
			if os.path.getsize(file) < SIZE_MB_20:
				break


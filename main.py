from image_generator import Generate_image
from aiogram.utils import executor


image_bot = Generate_image()
# Initialize the database and start the bot
image_bot.initialize_database()
executor.start_polling(image_bot.message_dispatcher, skip_updates=True)
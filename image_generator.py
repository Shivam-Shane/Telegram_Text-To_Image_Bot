from diffusers import StableDiffusionPipeline
import torch
import time
from datetime import datetime
import sqlite3
from aiogram import Bot, Dispatcher, types
from collections import defaultdict
from io import BytesIO
from better_profanity import profanity
import re
from utility import read_yaml
from logger import logging

class Generate_image():
    def __init__(self):
        self.config = read_yaml("config.yaml")
        self.model = self.config.get('model')

        # Initialize rate limit dictionary to track user request timing
        self.user_last_request_time = defaultdict(int)
        self.RATE_LIMIT = 5  # in seconds
        self.DATABASE_PATH = 'user_conversations.db'
        self.MAX_REQUEST_LIMITS = 20

        # Initialize StableDiffusionPipeline
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model, torch_dtype=torch.float16)
        if torch.cuda.is_available():
            self.pipe = self.pipe.to("cuda")

        # Set up Telegram bot and dispatcher as instance variables
        self.bot = Bot(token=self.config.get('telegram_bot_token'))
        self.message_dispatcher = Dispatcher(self.bot)

        # Register message handlers
        self.register_handlers()

    # ----------------------------------------------------------------------------------------------------------
    # Connection management function
    def get_connection(self):
        try:
            conn = sqlite3.connect(self.DATABASE_PATH, timeout=10, check_same_thread=False)
            logging.debug("Database connection established")
            return conn
        except Exception as e:
            logging.error(f"Failed to connect to database: {str(e)}")
            raise e

    # Ensure the database and table exist
    def initialize_database(self):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    user_id INTEGER PRIMARY KEY,
                    total_requests INTEGER DEFAULT 0,
                    timestamp TEXT
                )
            ''')
            conn.commit()
        except Exception as e:
            logging.error(f"Error initializing database: {e}")
            raise e
        finally:
            conn.close()

    # Check if the text contains profanities (outputs 1 for profane, 0 for clean)
    def contains_nsfw(self, content):
        logging.debug("Checking if the text contains is NSFW")
        return profanity.contains_profanity(content)

    def register_handlers(self):
        """Register command and message handlers with the dispatcher."""
        self.message_dispatcher.register_message_handler(self.botstarter, commands=["start"])
        self.message_dispatcher.register_message_handler(self.helper, commands=["help"])
        self.message_dispatcher.register_message_handler(self.greet_user, 
                                                         lambda message: re.search(r'\b(hi|hello|hey|hola|howdy|greetings|yo)\b', message.text.lower()))
        self.message_dispatcher.register_message_handler(self.image_generator)

    # Define /start command handler
    async def botstarter(self,message: types.Message):
        await message.reply("Hello! I'm a simple AI bot that will generate images from text. Send me a message to get started.")

    # Define /help command handler
    async def helper(self,message: types.Message):
        helper_commands = """Hello! I'm a simple AI bot that will generate images from text.
        /start - Start the bot
        /clear - Clear the conversation
        /help - Display this list of commands
        All Images generated will be in PNG format
        """
        await message.reply(helper_commands)

    # Define handler for greetings
    async def greet_user(self,message: types.Message):
        user_name = message.from_user.first_name
        greeting_message = f"Hello {user_name}! I can help you create realistic image from text, just provide a meaningful sentence and i will try my magic to create image? 😊"
        await message.reply(greeting_message)

    # Define handler for generating images
    async def image_generator(self, message: types.Message):
        conn = self.get_connection()  # Get database connection
        cursor = conn.cursor()
        user_id = message.from_user.id
        prompt = message.text
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_name = message.from_user.first_name

        try:
            cursor.execute('SELECT user_id, total_requests, timestamp FROM conversations WHERE user_id = ?', (user_id,))
            user_data = cursor.fetchone()

            if user_data is None:
                cursor.execute('INSERT INTO conversations (user_id, total_requests, timestamp) VALUES (?, ?, ?)',
                               (user_id, 0, timestamp))
                conn.commit()
                user_data = (user_id, 0, timestamp)

            total_requests, last_timestamp = user_data[1], user_data[2]
            current_day = datetime.now().strftime('%Y-%m-%d')

            if last_timestamp.split(' ')[0] != current_day:
                total_requests = 0
                cursor.execute('UPDATE conversations SET total_requests = ?, timestamp = ? WHERE user_id = ?',
                               (total_requests, timestamp, user_id))
                conn.commit()

            if total_requests >= self.MAX_REQUEST_LIMITS:
                await message.reply(f"{user_name}, you have reached your daily limit of {self.MAX_REQUEST_LIMITS} requests. Please try again tomorrow 😊.")
                return

            current_time = time.time()
            if current_time - self.user_last_request_time[user_id] < self.RATE_LIMIT:
                await message.reply("You're sending requests too quickly! Please wait a moment before trying again.")
                return

            self.user_last_request_time[user_id] = current_time

            if len(prompt) > 30:
                if self.contains_nsfw(prompt):
                    await message.reply("Your prompt contains inappropriate content. Please try again with a different prompt.")
                    return

                await message.reply("Generating your image, please wait...")

                # Generate the image
                image = self.pipe(prompt).images[0]
                img_byte_array = BytesIO()
                image.save(img_byte_array, format="PNG")
                img_byte_array.seek(0)

                # Increment and update the user's request count
                total_requests += 1
                cursor.execute('UPDATE conversations SET total_requests = ?, timestamp = ? WHERE user_id = ?',
                               (total_requests, timestamp, user_id))
                conn.commit()

                await message.reply_photo(photo=img_byte_array)
                await message.reply("A good writer writes a well Book")

            else:
                await message.reply("Please enter a valid prompt; the prompt is too small for creation.")

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            await message.reply("An error occurred while generating the image. Please try again.")

        finally:
            conn.close()
            logging.info("Database connection closed")


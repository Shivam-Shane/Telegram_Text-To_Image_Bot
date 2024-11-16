# Telegram Image Generation Bot

## Overview
This is a Telegram bot that generates images from text descriptions using a Large Language Model (LLM). Users can interact with the bot to create custom images based on their text prompts.

## Features
Image Generation: Users send a text description, and the bot generates an image based on that prompt.
High-Quality Outputs: Generated images are designed to be high-quality and can be downloaded directly from Telegram.
Safe Content: The bot generates user-friendly and non-adult content
Secure: Uses secure API connections to handle requests.

## Error Handling:

The system includes error handling mechanisms to manage cases where the content doesn't match any rule or if any other issue arises, while creating the image

## Requirements
- **Python 3.11+**
- **Telegram Bot API Token: You can obtain this by creating a bot on Telegram through BotFather**
- **Additional Libraries**: Listed in `requirements.txt`
- **SQLlite database**

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Shivam-Shane/Telegram_Text-To_Image_Bot.git
    pip install -r requirements.txt
    python main.py
    make sure to update config.yaml for the bot token 
    ```

## Usage
Start the Bot: Open Telegram and start a chat with your bot by searching for its username.
Send a Text Prompt: Type a description of the image you want to generate (e.g., "A futuristic cityscape at sunset").
Receive the Image: The bot will process your request and send you an image based on your prompt.
    ```
## Commands
/start: Initiates the bot and provides basic information on how to use it.
Text: [description]: Generate an image based on the given description.
/help: Provides a list of available commands and instructions.

## Logs:

All actions and errors are logged for troubleshooting and auditing purposes. Check the logs/ directory for log files.

## Future Enhancements
Add Customizable Image Styles: Allow users to choose specific art styles or aesthetics.
Support for Different Resolutions: Offer different image resolutions for various uses.
Error Handling: Improve error messaging and response times.

## Contribution
Feel free to fork this project, submit pull requests, or report issues. Contributions to enhance the functionality and make the system more robust are welcome!

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.

## Contact
For any questions or support, please contact the project maintainer at sk0551460@gmail.com

## Support the Project
Help us continue developing and improving this project by:

### Following Us on Social Media: 

Stay updated with our latest work by following us on LinkedIn at https://www.linkedin.com/in/shivam-2641081a0/

Buying Me a Book: https://buymeacoffee.com/shivamshane

# Acknowledgments
Telegram Bot API
LLM dreamlike-art
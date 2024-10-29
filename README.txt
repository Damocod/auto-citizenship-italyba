AutoCitizenshipItalyBA_v1.0.0

This bot is designed to help users secure an appointment for the Italian citizenship process
through reconstruction at the Italian consulate in Buenos Aires, Argentina.

Requirements:
- Operating System: Windows (I only tested on Windows 10)
- Google Chrome (I only tested on versión 129.0.6668.90 - Official Build - 64 bits)
- Internet Access: Required to access the appointment booking website
- Ensure that the .exe file and config.ini are in the same folder
- Before running this bot for the first time, some configuration needs to be done.

Configuration:
- Rename config.ini.example file to config.ini if it is not done yet.
- Open config.ini with a text editor.
- Set your Prenotami credentials and any other configurations.
- The media file that can be chosen in config.ini works as an alarm
  that activates when an available appointment is found, to get your attention
  in case you are not looking at the window in which the bot is operating.
- Remember to save any changes made to config.ini before proceeding.

Running the Bot:
- After configuring, run the .exe file (if it was already running, close it and run it again).
- The bot will attempt to access the appointment page in the Chrome browser continuously
  until it succeeds (at which point the user must continue the process manually)
  or until it is closed by the user.

Note: Most errors encountered are due to issues with Prenotami and not the bot itself.

Ciao.

This project is licensed under the MIT License
# Auto-Citizenship - ItalyBA

Python bot to help the user find available appointments for the Italian citizenship reconstruction procedure at the Italian Consulate in Buenos Aires, Argentina, through **Prenot@Mi** website. 

## Requirements:
- **Windows Operating System** (I only tested on Windows 10)
- **Google Chrome** (I only tested on versión 129.0.6668.90 - Official Build - 64 bits)
- **Internet Access** (Required to access the appointment booking website)
- Ensure that the `.exe` file and `config.ini` are **in the same folder**
- Before running this bot for the first time, some **configuration** needs to be done.

## Clone or Download

### Clone

```bash
git clone https://github.com/Damocod/auto-citizenship-italyba.git
```
### Download
- [Source code as ZIP file]("https://github.com/Damocod/auto-citizenship-italyba/archive/refs/heads/main.zip)
- [Executable version](https://github.com/Damocod/auto-citizenship-italyba/releases)

## Configuration:
1. If you see `config.ini.example` file raname it to `config.ini`.
2. Open `config.ini` with a text editor.
3. Set your Prenot@Mi credentials and any other configurations.
    > The media file that can be chosen in `config.ini` works as an alarm
      that activates when an available appointment is found, to get your attention in case you are not looking at the window in which the bot is operating.
4. Remember to save any changes made to `config.ini` before proceeding.

## Running the Bot:
1. After making the necessary configurations, run `main.py` (or the executable `.exe` file). If it was already running, close it and run it again.
2. The bot will attempt to access the appointment page in the Chrome browser continuously until it succeeds (at which point **the user must continue the process manually**) or until it is closed by the user.

## Notes
- Most errors encountered are due to issues with Prenot@Mi website and not the bot itself.
- I don't know if Prenot@Mi has any policy and/or system that punishes the use of bots or even the repeated and constant attempts to access the appointment request page. Use this bot at your own risk.
---

Chiao (°◡°)

This project is licensed under the MIT License.

© 2024 Auto-Citizenship - ItalyBA. All Rights Reserved.
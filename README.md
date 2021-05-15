# JstrisBot

AI that plays Tetris through [jstris.jezevec10.com](https://jstris.jezevec10.com/)

## Disclaimer

I do not condone cheating, this is a script made for learning purposes only, use it at your own risk. This script only works in Sprint (singleplayer) mode and won't work in Live (multiplayer) mode.

## Instructions

1. Clone this repository:

    `git clone https://github.com/jackweatherford/JstrisBot.git`

2. Enter the newly created directory:

    `cd JstrisBot`

3. Install the required Python modules:

   `pip install -r requirements.txt`

4. Run jstrisBot.py (with Python >= 3.0):

    `python jstrisBot.py`

5. Navigate to [jstris.jezevec10.com](https://jstris.jezevec10.com/) in your favorite web browser.
6. Start a game of Jstris in Sprint mode.
7. If the game is over and/or you want to restart, you must enter Ctrl + C in your terminal and re-run the bot before starting a new game.

### Troubleshooting

If you are experiencing any issues - make sure your Jstris Settings match the default:

![Control Settings](https://i.imgur.com/68judmL.png)

![Game Settings](https://i.imgur.com/ztSXAi0.png)

![Skin Settings](https://i.imgur.com/XmjmxKN.png)

Also be aware of PyAutoGUI's fail-safe: If you move your mouse to a corner of your screen - the program will terminate.

Additionally I have not programmed the bot to deal with holes in the structure - so it may stop working if all possible moves create holes.

For any other problems - please create a new issue in the repository or contact me directly.

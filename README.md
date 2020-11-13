This is a AI game called **Reversi (Modified)**.  

**Bibliography:**
Python version: 3.7.
Python Libraries:
	**Numpy**  https://numpy.org/citing-numpy/

**Instructions:** 
To start the game, go directly to 'main.py' file and run it. 
You would have an AI friend to play with you.  And you could determine how strongly your AI friend is.
You should choose your desired board size and number of blocks (obstacles) by entering integers when asked to. 
You could  enter "Y" or "N" to choose whether you want to play first. 
After the game starts, at each turn, choose a valid position to put your piece by entering the index (e.g., from 1 to 8) in the list of actions provided.

**Rules:** 
This is a two-player strategy board game, played on a square uncheckered board. 
At the beginning of the game, 2 white and 2 black pieces are put in the center of the board. 
Players take turns putting one white or black Reversi piece on the board. Each player can only use one color. 
Players should always put their pieces on the board so that two of them can form a straight line (horizontal, vertical, or diagonal). 
At the end of each turn, any opposite-colored pieces that exist within the line would be reversed to be the player’s color (white to black, black to white). 
The game ends when there’s no available space to put any pieces, or when for one player there’s no position to put so that at least one of opponent’s pieces would get reversed. 
Player with more pieces on the board would be the winner.

**Modified rule:** 
At the beginning of the game, random “obstacle” grids would appear on the board. 
Any lines that include the obstacle grids would not be reversed. 
Players cannot put any pieces on the obstacle positions.

**Your AI Friends:**
Easy mode: Uniformly Random model.
\\Hard mode: Minimax Tree Model


**Good luck and have fun\!** 


# ChessAI
My first foray into Deep RL


chess1.py was my first attempt at an algorithm. It tried to classify the value of the board by predicting whether the current state was likely to win. It went 50/50 against the "take random action" agent, and occationally drove off a cliff and consistently lost against the worst possible agent that isn't actively trying to lose. 

chess2.py is my 2nd attempt, ~6 months later. This time I'm using proper RL, starting with PPO. Instead of having the moves baked in, I'm going to have the output be 2 spots on the board. First the agent will be rewarded whenever it makes a legal move. 

# 🚀 Six Men's Morris using Minimax Algorithm
## Minimax Algorithm with Alpha-Beta Pruning

Six Men's Morris is a classic strategy board game dating back to ancient times. 
It's a two-player game played on a grid where players take turns placing their pieces and attempting to form rows of three (a "mill") to capture their opponent's pieces. 

### 🎨 This program was developed using Pygame for UI
![image](https://github.com/Tahmwellrups/six_men_morris/assets/130148168/20eca3ef-61c3-44ac-98db-87053da83159)

### ⚡️ Gameplay
Placement Phase (Phase 1)
![image](https://github.com/Tahmwellrups/six_men_morris/assets/130148168/8b386e6e-b542-4908-8cb8-661d03c7c3fa)

In the placement phase, you have six pieces that you can place anywhere in the board. But of course, the goal is to create a mill and reduce the AI's pieces. The AI will also have the same goal, so you have to prevent each other from forming a mill. At the upper left, you will see how many pieces you and the AI have left and will only be shown in the placement phase. 

Movement Phase (Phase 2)
![image](https://github.com/Tahmwellrups/six_men_morris/assets/130148168/43226ea7-8366-4122-a7f4-ae11f6d0d2c4)

In the movement phase, click the piece that you want to move and it will be highlighted. Only the pieces with an empty adjacent space will be allowed to move.

Fly Phase (Phase 3)
![image](https://github.com/Tahmwellrups/six_men_morris/assets/130148168/e6c39137-d0e4-4d18-b02c-83519df0c08c)
![image](https://github.com/Tahmwellrups/six_men_morris/assets/130148168/91e4f2bb-6e83-499c-afc5-8bb040e7d692)

The third phase will happen when you have three pieces left, you can literally move anywhere in the board, only exclusive to the player that has three pieces left.

AI's Algorithm
I used minimax algorithm with alpha-beta pruning for the AI to evaluate the board and the moves to check for potential mill and potential threats. The weights of the board, I experimented the values since I don't have reference on what should be the weights, I just followed the priority spaces in the game.

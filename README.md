# GNCA_invader

## GNCA Invader Game
This game was presented at the ALIFE 2023 workshop. 
As a preliminary implementation of GNCA to video games, Python was used for running neural network models, and Unity for running the game. The implemented game here is inspired by the classic Space Invaders from 1978. In the original game, space fighters shoot aliens. We replaced aliens with a GNCA lizard and the player aims to defeat the lizard by eliminating all its cells. The game was developed by `Takahide Yoshida` and `Hiroki Sato`. For more information, see `Automata Quest: NCAs as a Video Game Life Mechanic` by Hiroki Sato,　`Tanner Lund`, and Takahide Yoshida.

## Architecture

## How to Run
### Python Requirements
```sh
pip install numpy  
pip install json  
pip install onnxruntime  
```

### Instructions for Mac Users
```sh
git clone https://github.com/IkegLab/GNCA_invader.git
cd for_mac
python main.py
```
After that, tun  `for_mac.app`

### Instructions for Windows Users
```sh
git clone https://github.com/IkegLab/GNCA_invader.git
cd for_win/GNCA-ORT
python main.py
```
After that, run `nca_unity.exe`

## Features of this demo
This demo applies ALIFE research to games and offers new insights into the fields of gaming and ALIFE. In games where the termination condition is not binary, like our shooting game using NCA, it is difficult to create a unique winning strategy. The lizards of the NCA have weaknesses, but in some cases attacking them can result in further proliferation or changes in shape, making prediction difficult and adding a different type of dynamism than the semi-randomness of game genres like rogue-likes. 

Through the autonomy and robustness of life that the field of artificial life has continued to research, we can create endless games that don't bore players and do not have a unique winning strategy. NCAs have potential not only for representations of one character, but perhaps also many. NCAs could represent a large swarm of semi-independent enemies. Whether this were an action game, a zombie game, or some other type with many enemies, a swarm that can regenerate at a certain pace would make for an interesting challenge or interaction. Indeed, destructible environments could also benefit from such behavior: the walls of an "organic" building, for example. Opportunities abound.

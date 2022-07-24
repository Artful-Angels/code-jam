<img src="https://user-images.githubusercontent.com/65498475/180652320-46cf78bb-ecd0-4305-a37c-09fb9bdea69b.svg" alt="BugSweeper logo" width="500">

A minesweeper game with totally no bugs

---

# Introduction #

BugSweeper is a multiplayer minesweeper game made for the Python Discord code jam 9 using the websockets technolegy

The game contains absolutely no bugs at all

---
# How do I play
- `Creating a game` Press "new game" to generate a new game, enter your nickname and press "join"  

- `Joining a game` Enter a game code, enter your nickname and press "join"

- `Taking a turn` You can flag unlimited squares in your turn, and it will be only visible to you. You can only open **one** square per turn, and the turn will pass on to the next person

- `Winning` You will win in when you are the last person in the game

- `Loosing` You will lose in two circumstances:
  1. You open a mine
  2. You close the web window

<details>
<summary>Spoiler</summary>

* `Bugs` Events can be discovered through posting in the chat

   <details>
   <summary>List of bugs</summary>

   1. del x, y
   2. tnt

   </details>
   </details>

---
# Installation #
Using docker:
```shell
docker-compose up --build
```
Manual running:

Shell 1:
```shell
cd frontend
npm install
npm run dev
```
Shell 2:
```shell
cd backend
pip install -r requirements.txt
```
---
# Technologies used

1. Django Channels - We use Django Channels as our websocket library, used for frontend and backend connection
2. Vue.js - We use Vue.js as our main frontend technology
3. Docker - We use docker as our main packaging system

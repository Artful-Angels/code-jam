<img src="https://user-images.githubusercontent.com/65498475/180652320-46cf78bb-ecd0-4305-a37c-09fb9bdea69b.svg#gh-light-mode-only" alt="BugSweeper logo" width="500">
<img src="https://user-images.githubusercontent.com/65498475/181659011-5d3aa919-1dcf-4507-b443-2d9ca8d25641.svg#gh-dark-mode-only" alt="BugSweeper logo" width="500">


A minesweeper game with totally no bugs.

---

## Introduction

BugSweeper is a multiplayer minesweeper game made for the Python Discord code jam 9 using the websockets technology.

---
## How do I play?

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

  1. "delete" - Reveals an open and safe square
  2. "winner" - Chance to kill all other players

  </details>
</details>

---
## Dev installation

Using docker:
```shell
docker-compose up --build
```
Note: You need to have the desktop Docker app, download it from https://docs.docker.com/get-docker/

---
## Technologies used

1. Django Channels - We use Django Channels as our websocket library, used for frontend and backend connection
2. Vue.js - We use Vue.js as our main frontend technology
3. Docker - We use docker as our main packaging system

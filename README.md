<img src="https://user-images.githubusercontent.com/65498475/180652320-46cf78bb-ecd0-4305-a37c-09fb9bdea69b.svg#gh-light-mode-only" alt="BugSweeper logo" width="500">
<img src="https://user-images.githubusercontent.com/65498475/181659011-5d3aa919-1dcf-4507-b443-2d9ca8d25641.svg#gh-dark-mode-only" alt="BugSweeper logo" width="500">


A minesweeper game with totally no bugs.

---

## Introduction

BugSweeper is a multiplayer minesweeper game made for the Python Discord code jam 9 using the websockets technology.

---
## How do I play?

Go to https://bugsweeper.godi.se and choose your nickname!

- `Creating a game` Press "new game" to generate a new game code and press "join".

- `Joining a game` Enter a game code of an existing game (that hasn't started) and "join".

- `Taking a turn` Turns rotate between living players. You can only open **one** square per turn.

- `Flagging` You can flag any closed squares. Flags are only visible to you.

- `Winning` If all safe squares are uncovered then all remaining players will win.

- `Losing` You will die in two circumstances:
  1. You click on a mine, which will then become visible to all other players.
  2. Eliminated through the successful use of the `winner` command (see more below)!


## Bugs

Bugs can be discovered through posting any of the following commands in the chat:

- **"delete"** - Deletes the cover of a random square that is both closed and safe (thus opening it). Counts as a turn and can only be used 5 times per player.
- **"close"** - Closes all squares. Can only be used once in a game by a dead player.
- **"new"** - Gives a 1 in the number of players chance to give the player new life. Can only be used once per player (and if they're dead).
- **"winner"** - Gives a variable chance to eliminate all other players (although they have a chance of coming back using "new"). The chance is 1 in twice the number of living players who haven't used the command. Can only be used once per player.


---
## Dev installation

Using docker:
```shell
docker-compose up --build
```
Note: You need to have the desktop Docker app, download it from https://docs.docker.com/get-docker/

---
## Technologies used

- Django Channels as our websocket library for both the frontend and backend connection.
- Docker as our main packaging system, which helped us work with different operating systems.
- Vue.js as our main frontend technology.

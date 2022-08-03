<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/65498475/181659011-5d3aa919-1dcf-4507-b443-2d9ca8d25641.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/65498475/180652320-46cf78bb-ecd0-4305-a37c-09fb9bdea69b.svg">
  <img alt="BugSweeper logo" width="500" src="="https://user-images.githubusercontent.com/65498475/181659011-5d3aa919-1dcf-4507-b443-2d9ca8d25641.svg">
</picture><hr>

[![MIT License](https://img.shields.io/github/license/Artful-Angels/code-jam)](https://github.com/Artful-Angels/code-jam/blob/main/LICENSE) [![Linting](https://github.com/Artful-Angels/code-jam/actions/workflows/lint.yaml/badge.svg)](https://github.com/Artful-Angels/code-jam/actions/workflows/lint.yaml) [![Netlify status](https://api.netlify.com/api/v1/badges/5ed196e8-5c53-4afb-a00f-977ce3bcfdf0/deploy-status)](https://app.netlify.com/sites/bugsweeper-dev/deploys)

A modern minesweeper game with totally no bugs.

BugSweeper is a multiplayer minesweeper game made for the Python Discord Summer Code Jam 9, with WebSockets as the technology and the theme "it's not a bug, it's a feature".


## Table of contents

- [Preview](#preview)
  - [Lobby](#lobby)
  - [Active game](#active-game)
  - [Commands list](#commands-list)
- [How to play](#how-to-play)
  - [Bugs](#bugs)
- [Dev installation](#dev-installation)
- [Technologies used](#technologies-used)


## Preview

<note>

**Note**: this readme updates the images to match your system theme (dark or light mode), just like the website.

</note>

### Lobby
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/65498475/182606217-444f7e83-7c92-45e6-9b9b-abe289919a38.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/65498475/182606302-def0c144-e147-4990-95fb-2a188f983a69.png">
  <img alt="Lobby demo" src="https://user-images.githubusercontent.com/65498475/182605418-a0c26207-5b7c-4849-a649-ec588e68b9f8.png">
</picture>

### Active game

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/65498475/182603512-134b03f2-1236-4bc2-9e4a-d7deed56cd9a.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/65498475/182604532-8eab598e-d228-43f1-aec8-c312497ec6a1.png">
  <img alt="Active game demo" src="https://user-images.githubusercontent.com/65498475/182605653-9cc1a8ed-4fb5-4037-9f02-357517f2faa7.png">
</picture>


### Commands list

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/65498475/182605242-4084cf70-3f1a-48fb-b903-59387a6f2213.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/65498475/182605418-a0c26207-5b7c-4849-a649-ec588e68b9f8.png">
  <img alt="Commands list demo" src="https://user-images.githubusercontent.com/65498475/182605242-4084cf70-3f1a-48fb-b903-59387a6f2213.png">
</picture>


## How to play?

Go to [bugsweeper.godi.se](https://bugsweeper.godi.se) and choose a nickname to get started!

- `Creating a game` - Press "new game" to generate a new game code, which you can share with your friends
- `Joining a game` - Enter the game code of an existing game (where no squares have been opened yet) and press `JOIN`
- `Taking a turn` - Turns rotate between living players. You can only open **one** square per turn
- `Flagging` - You can flag any closed squares by right clicking on them. Flags are only visible to you
- `Winning` - Everyone who manages to survive until the board doesn't have any unopened non-mine squares win!
- `Losing` - You will die under two circumstances:
  1. You click on a mine, which will then become visible to all other players
  2. Eliminated through the successful use of the `winner` command (see more below)!


### Bugs

Bugs can be discovered through posting any of the following commands in the chat:

- `delete` - Deletes the cover of a random square that is both closed and safe (thus opening it). Counts as a turn and can only be used 5 times per player
- `close` - Closes all squares. Can only be used once in a game by a dead player
- `new` - Gives a 1 in the number of players chance to give the player new life. Can only be used once per player (and if they're dead)
- `winner` - Gives a variable chance to eliminate all other players (although they have a chance of coming back using "new"). The chance is 1 in twice the number of living players who haven't used the command. Can only be used once per player

The current list of commands can be found at [bugsweeper.godi.se/commands](https://bugsweeper.godi.se/commands)


## Dev installation

Using docker:
```shell
docker-compose up --build
```
Note: You need to have the desktop Docker app, download it from https://docs.docker.com/get-docker/


## Technologies used

The application approximately follows the architecture described in [this Miro board](https://miro.com/app/board/uXjVOj0M0wU=/?share_link_id=644032710468). The frameworks used are as follows:

- Django Channels for the backend, allowing it to communicate over both HTTP and WebSockets
- Redis for storing data
- Docker as our main packaging system, which makes development OS-agnostic and simplified the setup process
- Vue.js for the frontend

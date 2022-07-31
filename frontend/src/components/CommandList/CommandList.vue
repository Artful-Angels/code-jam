<template>
  <main class="bg-white dark:bg-slate-800 h-auto p-7 rounded-lg">
    <div class="mb-11">
      <a href="/" class="text-blue-600 hover:text-blue-700">← Go back home</a>
      <h2 class="text-left mb-3 mt-1">Commands</h2>
      <p class="dark:text-gray-200">Bugs have a tendency to be unreliable, so some commands can only be used a certain number of times, or only have a certain chance of working. As you might know, not even the developers know all the bugs, so there are some commands that you won't even find in this list!</p>
    </div>
    <div>
      <CommandListCommand
        v-for="command in commands"
        :key="command.name"
        v-bind="command"
      />
    </div>
  </main>
</template>

<script setup>
import CommandListCommand from "@/components/CommandList/CommandListCommand.vue";

const commands = [
  {
    name: "delete",
    description: "Opens a random square on the board",
  },
  {
    name: "close",
    description: "Closes all squares on the board. Can only be run by a dead player, once per game",
  },
  {
    name: "new",
    description: "Gives the player a new life. Can only be used once per game",
    isHidden: true,
  },
  {
    name: "winner",
    description: "Gives the player a small chance of winning. Can only be run by a dead player, once per game",
    isHidden: true,
  },
]
</script>

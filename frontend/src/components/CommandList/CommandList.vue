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
    description: "Deletes the cover of a square that is both closed and safe. Counts as a turn and can only be used 5 times per player.",
  },
  {
    name: "close",
    description: "Closes all squares. Can only be used once in a game by a dead player.",
  },
  {
    name: "new",
    description: "Gives a 1 in the total number of players chance to give a player new life. Can only be used once per player.",
  },
  {
    name: "winner",
    description: "Gives a variable chance to eliminate all other players (although they have a chance of coming back using new). The chance is 1 in twice the number of living players who haven't used the command. Can only be used once per player.",
  },
]
</script>

<template>
  <div class="mt-20">
    <div class="text-center flex flex-col items-center">
      <h2 class="mb-2">Waiting for players...</h2>
      <p class="dark:text-gray-300 mb-6">
        Share this code with your friends to let them join the game:
      </p>
      <div
        data-tooltip-target="tooltip-default"
        class="max-w-sm hover:cursor-pointer py-2 px-5 rounded-md bg-gray-50 dark:bg-slate-800 dark:border-slate-700"
        @click="copyToClipboard(gameCode)"
      >
        <p class="text-6xl font-bold text-gray-900 dark:text-gray-200">
          {{ gameCode }}
        </p>
      </div>
    </div>
    <div class="flex justify-center mt-10">
      <LogoIcon class="max-w-[96px] animate-bounce" />
    </div>
  </div>
</template>

<script setup>
import LogoIcon from "@/components/logos/LogoIcon.vue";

const props = defineProps({
  gameCode: {
    type: Number,
    required: true,
  },
});

function copyToClipboard(text) {
  navigator.clipboard.writeText(text.toString());
}
</script>

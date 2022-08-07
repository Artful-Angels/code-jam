<template>
  <div
    data-tooltip-target="tooltip-default"
    class="max-w-md hover:cursor-pointer py-3 px-5 rounded-md bg-gray-50 dark:bg-slate-800 dark:border-slate-700"
    @click="copyToClipboard(copyText)"
  >
    <p
      class="text-4xl font-bold text-gray-800 hover:text-gray-900 dark:text-gray-300 hover:dark:text-gray-200 uppercase"
    >
      {{ copyText }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  copyText: {
    type: String,
    required: true,
  },
});

function copyToClipboard(text) {
  navigator.clipboard.writeText(text.toString());
}
</script>

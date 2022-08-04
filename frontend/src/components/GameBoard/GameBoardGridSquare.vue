<template>
  <button
    class="flex items-center place-content-center p-1 rounded-md aspect-square"
    :class="{ 'bg-gray-100 dark:bg-slate-800': !is_open }"
    @click="openSquare"
    @contextmenu.prevent="$emit('toggleFlag', coordinates)"
    :disabled="disabled || is_open"
  >
    <Flag v-if="flagStatus === 1 && !is_open" />
    <FlagSafe v-else-if="flagStatus === 2 && !is_open" />
    <Mine v-else-if="is_open && is_mine" />
    <span v-else-if="is_open" class="my-[-10px] dark:text-gray-300">{{
      adjacent_mines ? adjacent_mines : ""
    }}</span>
  </button>
</template>

<script setup>
import Flag from "@/components/icons/Flag.vue";
import Mine from "@/components/icons/Mine.vue";
import FlagSafe from "@/components/icons/FlagSafe.vue";

const emit = defineEmits(["openSquare", "toggleFlag"]);

const props = defineProps({
  coordinates: {
    type: Array,
    required: true,
  },
  is_open: {
    type: Boolean,
    required: false,
    default: false,
  },
  is_mine: {
    type: Boolean,
    required: false,
    default: false,
  },
  flagStatus: {
    type: Number,
    required: false,
    default: 0,
  },
  disabled: {
    type: Boolean,
    required: false,
    default: false,
  },
  adjacent_mines: {
    type: Number,
    required: false,
    default: 0,
  },
});

function openSquare() {
  if (props.flagStatus !== 1 && !props.is_open) {
    emit("openSquare", props.coordinates);
  }
}
</script>

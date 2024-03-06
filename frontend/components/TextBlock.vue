<script setup lang="ts">
defineProps<{
  text: {
    type: string
    required: true
  }
}>()
</script>

<template>
  <div
    class="flex flex-col content-center items-center justify-center py-8 text-center"
  >
    <div class="w-[300px] text-base sm:text-lg md:w-[480px]">
      {{ text }}
    </div>
  </div>
</template>

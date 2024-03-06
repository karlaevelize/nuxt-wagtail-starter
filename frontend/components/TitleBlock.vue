<script setup lang="ts">
const props = defineProps<{
  title: {
    type: string
    required: true
  }
  type: {
    type: string
    required: true
  }
}>()

const headerClasses = computed(() => {
  return {
    'text-3xl': props.type === 'h1',
    'text-2xl': props.type === 'h2',
    'text-xl': props.type === 'h3',
    'text-lg': props.type === 'h4',
    'text-md': props.type === 'h5',
    'text-sm': props.type === 'h6',
  }
})
</script>

<template>
  <h2 :class="['py-3 font-semibold tracking-widest', headerClasses]">
    {{ title }}
  </h2>
</template>

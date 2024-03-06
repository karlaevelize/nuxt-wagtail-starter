<script setup lang="ts">
defineProps({
  image: {
    type: Object,
    required: true,
  },
})

const config = useRuntimeConfig()
</script>

<template>
  <div class="px-2 py-7">
    <img
      class="mx-auto aspect-square w-72 rounded-full grayscale"
      :src="`${config.public.cmsAPI}/${image.details.src}`"
      :alt="image.details.alt"
    />
  </div>
</template>

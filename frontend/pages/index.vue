<script setup lang="ts">
const config = useRuntimeConfig()

const { data } = await useAsyncData(async () => {
  // Ignore eslint rule, otherwise we don't see errors from
  // this block when running on Docker.
  /* eslint no-useless-catch: "off" */
  try {
    const response = await $fetch(`${config.public.cmsAPI}/api/v2/pages`)
    return response
  } catch (error) {
    throw error
  }
})
</script>

<template>
  <div>
    <h1>mysite CMS</h1>
    <div v-if="!data">Loading...</div>
    <div v-else>
      <NuxtLink
        v-for="item in data.items"
        :key="item.id"
        :to="`/${item.meta.slug}`"
      >
        {{ item.title }}
      </NuxtLink>
    </div>
  </div>
</template>

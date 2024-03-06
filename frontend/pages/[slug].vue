<script setup lang="ts">
const route = useRoute()
const routeParams = new URLSearchParams(route.query)

const config = useRuntimeConfig()
const previewMode = route.path === '/@preview/'

const { data } = await useAsyncData(
  async () => {
    const url = previewMode
      ? `/api/v2/page_preview/0/?${routeParams}`
      : `${config.public.cmsAPI}/api/v2/pages/find/?html_path=${route.path}`

    // Ignore eslint rule, otherwise we don't see errors from
    // this block when running on Docker.
    /* eslint no-useless-catch: "off" */
    try {
      return await $fetch(url)
    } catch (error) {
      throw error
    }
  },
  {
    server: !previewMode,
  },
)

const components = {
  // base blocks
  title_block: defineAsyncComponent(
    () => import('/components/TitleBlock.vue'),
  ),
  generic_text_block: defineAsyncComponent(
    () => import('/components/TextBlock.vue'),
  ),
  image_block: defineAsyncComponent(
    () => import('/components/ImageBlock.vue'),
  ),
}
</script>

<template>
  <div class="mx-auto text-center">
    <div v-if="!data">This page has nothing to display</div>
    <template v-else>
      <component
        :is="components[block.type]"
        v-for="block in data.body"
        :key="block.id"
        v-bind="
          Array.isArray(block.value) ? { blocks: block.value } : block.value
        "
      >
      </component>
    </template>
  </div>
</template>

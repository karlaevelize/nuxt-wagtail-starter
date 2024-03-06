// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  devServer: {
    port: 3000,
  },
  app: {
    head: {
      title: 'My Site - Wagtail CMS',
    },
  },
  runtimeConfig: {
    public: {
      cmsAPI:
        process.env.NUXT_PUBLIC_SITE_CMS_API || 'https://www.mysite.test',
    },
  },
})

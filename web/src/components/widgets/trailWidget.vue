<template lang='pug'>
  #breadcrumb
    nav.breadcrumb.has-succeeds-separator.m-t-10(aria-label='breadcrumbs')
      ul
        li(v-for="(item, idx) in breadcrumbList" :key="item.path")
          // last item
          p(v-if="idx == breadcrumbList.length - 1") {{ item.meta.title }}
          router-link(v-else :to="item.path") {{ item.meta.title }}
</template>

<script>
export default {
  data() {
    return {
      breadcrumbList: []
    }
  },
  mounted() {
    this.updateBreadcrumb()
  },
  watch: { '$route' () { this.updateBreadcrumb() } },
  methods: {
    updateBreadcrumb() {
      // only show routes with meta.title
      let matched = this.$route.matched.filter(item => item.meta && item.meta.title)
      this.breadcrumbList = matched.filter(item => item.meta && item.meta.title && item.meta.breadcrumb !== false)
    },
  }
  
}
</script>

<style lang="scss" scoped>
  
.breadcrumb.has-succeeds-separator li + li::before {
  content: ">>";
}

li:first-child p {
  padding-left: 0;
}

p {
  padding: 0 0.75em;
}
</style>

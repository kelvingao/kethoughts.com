<template lang="pug">
  #app
    top
    router-view
</template>

<script>
import top from '@/components/layout/header.vue'
export default {
  name: "app",
  components: {
    top,
  }
};
</script>

<style lang="scss">
@import '@/sass/app.scss';

</style>

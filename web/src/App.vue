<template lang="pug">
  #app
    top
    router-view
    bottom
</template>

<script>
import top from '@/components/layout/header.vue'
import bottom from '@/components/layout/footer.vue'

export default {
  name: "app",
  components: {
    top,
    bottom
  }
};
</script>

<style lang="scss">
@import '@/sass/app.scss';

</style>

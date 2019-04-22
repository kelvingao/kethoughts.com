<template lang='pug'>
  #manage
    .columns.is-marginless.is-fullheight
      //- manage panel
      aside.is-narrow-mobile.is-fullheight.section.is-hidden-mobile
        manage-panel
      //- manage content
      .column
        breadcrumb-widget
        hr
        router-view

</template>

<script>
import ManagePanel from '@/components/manage/sidebar';
import BreadcrumbWidget from '@/components/widgets/breadcrumb';

export default {
  components:{
    ManagePanel,
    BreadcrumbWidget
  }
}
</script>

<style lang="scss">

aside {
  height: 100vh;
  background-color: whitesmoke;
}
</style>

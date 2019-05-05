<template lang='pug'>
  #manage
    .columns.is-marginless.is-fullheight
      //- manage sidebar
      aside.is-narrow-mobile.is-fullheight.section.is-hidden-mobile
        manage-panel
      //- manage content
      .column.manage-content
        breadcrumb-widget.m-b-20
        router-view

</template>

<script>
import ManagePanel from '@/components/manage/sidebar';
import BreadcrumbWidget from '@/components/widgets/trailWidget';

export default {
  components:{
    ManagePanel,
    BreadcrumbWidget
  }
}
</script>

<style lang="scss" scoped>

aside {
  height: 100vh;
}

.manage-content {
  background-color: whitesmoke;
}
</style>

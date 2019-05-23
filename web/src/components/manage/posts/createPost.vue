<template lang='pug'>
  #createPost
    edit-widget(:post='post')

</template>
<script>
import editWidget from '@/components/widgets/editWidget';

export default {
  name: 'CreatePost',
  components: {
    editWidget,
  },
  data() {
   return {
     post: {
        id: null,
        title: '',
        slug: '',
        content: '',
        excerpt: '',
        featured_image: '',
        status: 'draft'
      },
   }
  },
}
</script>

<style lang="scss" scoped>

</style>

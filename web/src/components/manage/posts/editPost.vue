<template lang='pug'>
  #editPost
    edit-widget(:post='post')

</template>
<script>
import api from '@/api';
import editWidget from '@/components/widgets/editWidget';

export default {
  name: 'EditPost',
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
        featured_image: ''
      },
    }
  },
  created() {
    api.getPostById(this.$route.params.id).then(res => {
      this.post = res.data
    })
    .catch(err => {
      console.log(err)
    })
  },

}
</script>

<style lang="scss" scoped>

</style>

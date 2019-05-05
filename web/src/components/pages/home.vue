<template lang="pug">
  #postsPage
    .home-container
      .container
        .post-container(:key="post.id" v-for="post in posts")
          .title
            router-link(:to="'/posts/' + post.slug") {{ post.title}}

          span.is-muted {{ post.modified | formatDate }} | by 
          router-link.is-muted(to='/#') {{ post.name }} 

          .content.m-t-10(v-html="post.content")
          hr.m-b-10
</template>

<script>
import api from '@/api'

export default {
  name: 'Home',
  data() {
    return {
      posts:[],
    }
  },

  beforeCreate() {
    api.getPosts().then(res => {
      this.posts = res.data;
    })
    .catch(err => {
      console.log(err)
    })
  },
 
}
</script>

<style lang="scss" scoped>

/* Theme Name: Learning VueJs
Author: Kelvin Gao
Author URI: https://github.com/kelvingao
Version: 1.0
*/

</style>

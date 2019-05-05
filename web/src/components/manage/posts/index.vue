<template lang='pug'>
  #postsPage
    .flex-container
      .columns
        .column.m-r-30
          nav.level(v-if="showIndexPage")
            .level-left
              .level-item
                p.subtitle.is-5 #[strong {{ numPosts }} ] posts

              .level-item
                b-field.has-addons
                  p.control
                    input.input(type="text" placeholder="Find a post")
                  p.control
                    button.button Search

            .level-right
              p.level-item All
              p.level-item
                router-link(to="/#") Published
              p.level-item
                router-link(to="/#") Drafts
              p.level-item
                router-link(to="/#") Deleted
              p.level-item
                router-link.button.is-primary.is-pulled-right(to="/manage/posts/create")
                  i.fa.fa-user-plus.m-r-10
                  |  New Post
      table.table.is-narrow(v-if="showIndexPage")
        thead
          tr
            th id
            th Author
            th Title
            th Status
            th Created
            th Modified
            th Type
            th Actions
        tbody
          tr(v-for="post in posts")
            th {{ post.id }}
            td {{ post.name }}
            td {{ post.title }}
            td {{ post.status }}
            td {{ post.created | formatDate }}
            td {{ post.modified | formatDate }}
            td {{ post.type }}
            td
              router-link.button.is-info.is-outlined.m-r-5(:to="'/manage/posts/edit/' + post.id") Edit
              button.button.is-danger.is-primary.is-outlined(@click="del(post.id)") Delete
    router-view

</template>

<script>
import api from '@/api'

export default {
  name: 'Posts',
  data() {
    return {
      numPosts: 0,
      showIndexPage: this.$route.path == '/manage/posts' ? true : false,
      posts:[]
    }
  },
  watch: {
    '$route' () {
      this.showIndexPage = this.$route.path == '/manage/posts' ? true : false
      this.updateList()
    },
  },

  created() {
    this.updateList()
  },
  
  methods: {
    updateList() {
      api.getPosts().then((res) => {
        this.posts = res.data
        this.numPosts = res.length 
      })
    },

    del(id) {
      this.$dialog.confirm({
          title: 'Deleting post',
          message: 'Are you sure you want to <b>delete</b> this post?',
          confirmText: 'Delete Post',
          type: 'is-danger',
          hasIcon: true,
          size: 'is-normal',
          onConfirm: () => {
            api.deletePost(id).then(res => {
              this.$toast.open('Post deleted!')
              this.updateList()
            })
            .catch(err => {
              alert(err)
            })
              
          }
      })
    }
  },

}
</script>

<style scoped>

table {
  width: 100%;
}
</style>
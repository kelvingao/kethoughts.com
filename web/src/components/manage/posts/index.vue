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
            th Author
            th Title
            th Views
            th Created
            th Modified
            th Actions
        tbody
          tr(v-for="post in posts")
            td {{ post.name }}
            td 
              router-link(:to="'/posts/' + post.slug" style="text-decoration: underline") {{ post.title }}
              span(v-if="post.status == 'private'")  — Private
            td {{ post.views }}
            td {{ post.created | formatDate }}
            td {{ post.modified | formatDate }}
            td
              button.button.is-small.is-light.m-r-5(@click="edit(post.id)")
                b-icon(icon="pen" size="is-small")
              button.button.is-small.is-danger.is-primary(@click="del(post.id)")
                b-icon(icon="trash-alt" size="is-small")
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
      this.$route.path == '/manage/posts' ? ( this.showIndexPage = true, this.updateList()) : this.showIndexPage = false
    },
  },

  created() {
    this.updateList()
  },
  
  methods: {
    updateList() {
      api.getPosts('all').then((res) => {
        this.posts = res.data
        this.numPosts = this.posts.length
      })
    },

    edit(id) {
      this.$router.push('/manage/posts/edit/' + id)
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
              this.$toast.open({
                message: 'Post deleted!',
                type: 'is-primary'
              })
              this.updateList()
            })
            .catch(err => {
              console.error(err)
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
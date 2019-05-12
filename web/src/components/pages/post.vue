<template lang="pug">
  #post
    .post-container
      .container
        .title {{ post.title }}
        .content(v-html="post.content")
        hr

</template>

<script>
import api from '@/api'
const STATICDOMAIN = 'http://images.kethoughts.com'

export default {
  data() {
    return {
      post: {},
    }
  },
  beforeCreate() {
    api.getPostBySlug(this.$route.params.slug).then(res => {
      this.post = res.data;
    })
    .catch(err => {
      console.error(err)
    }),

    api.getWeixinJsSdk({ url: window.location.href }).then((res) => {
      wx.config({
        debug: true,
        appId: res.data.appid,
        timestamp: res.data.timestamp,
        nonceStr: res.data.noncestr,
        signature: res.data.signature,
        jsApiList: [
          'onMenuShareTimeline', 
          'onMenuShareAppMessage', 
          'onMenuShareWeibo'
        ]
      });
      wx.ready(() => {
        wx.onMenuShareTimeline({
          title: this.post.title,
          link: window.location.href,
          imgUrl: STATICDOMAIN + '/' + this.post.featured_image,
          success: function () {
              return
          },
          cancel: function () {
              return
          }
        })
      });
    })
    .catch(err => {
      console.error(err)
    })
  },

}
</script>

<style scoped>

#post {
  height: 100vh;
}
</style>



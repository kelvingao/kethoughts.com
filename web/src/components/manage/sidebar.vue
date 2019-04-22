<template lang='pug'>
  #sidebar
    p.menu-label.is-hidden-touch
      b-icon.m-r-5(icon="tachometer-alt" size="is-normal")
      | Dashboard
    ul.menu-list
      li
        router-link(to='/manage/analytics') Google Analytics
        
    p.menu-label.is-hidden-touch
      b-icon.m-r-5(icon="file-video" size="is-normal")
      | CMS Content
    ul.menu-list
      li
        router-link(to='/manage/posts') Blog Posts
        a.has-submenu Roles &amp; Permissions
        ul.submenu
          li
            router-link(to='/manage/roles') Roles
            router-link(to='/manage/permissons') Permissions

    p.menu-label.is-hidden-touch
      b-icon.m-r-5(icon="user-cog" size="is-normal")
      | Administration
    ul.menu-list
      li
        router-link(to='/manage/users') Manage Users
</template>

<script>

export default {
  mounted() {
    this.setSubmenuSlides()
  },

  methods: {
    setSubmenuStyles (s, height, margin) {  // s: submenu
      s.style.maxHeight = height
      s.style.marginTop = margin
      s.style.marginBottom = margin
    },

    setSubmenuSlides() {
      const accordions = this.$el.querySelectorAll('.has-submenu');
      // set slides to all has-subment elements
      for(var i=0; i< accordions.length; i++) {
        accordions[i].onclick = () => {
          // FIXME: classList is undefined!
          // this.classList.toggle('is-active');
          const submenu = this.$el.querySelector('.submenu');
          if (submenu.style.maxHeight) {
            this.setSubmenuStyles(submenu, null, null)
          } else {
            this.setSubmenuStyles(submenu, submenu.scrollHeight + "px", "0.75em")
          }
        }
      }
    }
  }
  
}
</script>

<style lang="scss" scoped>

.submenu {
  max-height: 0;
  overflow: hidden;
  transition: all 0.2s ease-in-out;
}

.menu-list li ul{
  margin-top: 0;
  margin-bottom: 0;
}
</style>

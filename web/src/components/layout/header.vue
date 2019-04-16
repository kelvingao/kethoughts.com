<template lang='pug'>
  #top
    nav.navbar.has-shadow.is-dark
      .container
        .navbar-brand.is-primary
          .navbar-item.is-expanded
            b-input(placeholder='Search...', type='search', icon='search' expanded)

          .navbar-burger.burger(@click="showNav = !showNav" :class="{'is-active' : showNav}")
            span
            span
            span

        .navbar-menu(:class="{ 'is-active' : showNav }")
          .navbar-start
            router-link.navbar-item.is-tab(to='/')
              b-icon.m-r-5(icon="home") 
              | Home
            router-link.navbar-item.is-tab(to='/tutorials')
              b-icon.m-r-5(icon="video") 
              | Tutorials
            router-link.navbar-item.has-dropdown.is-hoverable(to='/docs')
              .navbar-link
                b-icon.m-r-5(icon="book") 
                | Docs
              .navbar-dropdown
                router-link.navbar-item(to='/contact') Contact
                router-link.navbar-item(to='/about') About Me
                hr.navbar-divider
                router-link.navbar-item(to='/issue') Report an issue

          .navbar-end
            .navbar-item(v-if="!isAuthenticated")
              .buttons
                router-link.button.is-primary.is-outlined(to='/register') #[strong SignUp]
                router-link.button.is-primary.is-inverted(to='/login') #[strong Login]

            .navbar-item(v-else).has-dropdown.is-hoverable
              .navbar-link Hey, Kelvingao
              .navbar-dropdown.is-left
                router-link.navbar-item(to='/profile')
                  b-icon.m-r-5(icon='user-circle')
                  | Profile
                router-link.navbar-item(to='/notifications')
                  b-icon.m-r-5(icon='bell')
                  | Notifications
                router-link.navbar-item(to="/admin")
                  b-icon.m-r-5(icon='cog')
                  | Manage
                hr.navbar-divider
                router-link.navbar-item(@click.native="logout" to='/home')
                  b-icon.m-r-5(icon='sign-out-alt')
                  | Logout

</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  data() {
    return {
      showNav: false,
    }
  },
  computed: {
    ...mapGetters([
      'isAuthenticated'
    ])
  },
}
</script>

<style lang="scss" scoped>

  @media screen and (max-width: 1087px) {

    .control {
      width: 100%;
    }

    .navbar-item {
      padding-left: 5px;
      padding-right: 0px;
    }

  }
</style>

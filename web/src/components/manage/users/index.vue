<template lang='pug'>
  #users
    table.table
      thead
        tr
          th id
          th Name
          th Email
          th Role
          th Created
          th Last IP
          th Login Count
          th Actions
      tbody
        tr(v-for="user in users")
          th {{ user.id }}
          td {{ user.name }}
          td {{ user.email }}
          td {{ user.role_name }}
          td {{ user.created | formatDate }}
          td {{ user.last_ip }}
          td {{ user.login_count }}
          td
            router-link.button.is-outlined.m-r-5(to="/#") View
            router-link.button.is-outlined(to="/#") Edit
</template>

<script>
import api from '@/api'

export default {
  name: 'Users',
  data() {
    return {
      users: [],
    }
  },

  beforeCreate() {
    api.getUsers().then((res) => {
      this.users = res.data
    })
  },

}
</script>

<style lang="scss" scoped>

table {
  width: 95%;
}
</style>

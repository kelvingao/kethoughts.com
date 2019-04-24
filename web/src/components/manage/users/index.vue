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
          td {{ timestamp2str(user.created) }}
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

  beforeMount() {
    api.getUsers().then((resp) => {
      console.log(resp)
      this.users = resp
    })
  },

  methods: {
    timestamp2str(ts) {
      let datetime = new Date();
      datetime.setTime(ts * 1000);

      let year = datetime.getFullYear();
      let month = datetime.getMonth() + 1;
      let day = datetime.getDate();

      let hour = datetime.getHours();
      let minute = datetime.getMinutes();
      let second = datetime.getSeconds();

      return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second;
    }
  }
}
</script>

<style lang="scss" scoped>

table {
  width: 95%;
}
</style>

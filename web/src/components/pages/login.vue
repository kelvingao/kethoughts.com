<template lang='pug'>
  #login
    .column.is-one-third.is-offset-one-third.p-0
      .card.card-content
        h1.title Log In
        form(@submit="onSubmit" method="POST" role="form")
          b-field(label="Email Address")
            b-input(placeholder="name@example.com" type="email" icon="envelope" required v-model="form.email")
          b-field(label="Password")
            b-input(type="password" placeholder="Password regular input" icon="key" v-model="form.password")
          b-checkbox.m-t-15(v-model="form.checked") Remember Me
          button.button.is-primary.is-outlined.is-fullwidth.m-t-20 Log In

      h5.has-text-centered.m-t-20
        router-link.is-muted(to="") Forgot Your Password?
   
</template>
<script>

export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: '',
        checked: false
      },
      token:'',
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
    //   alert(JSON.stringify(this.form))

      const { email, password } = this.form
      this.$store.dispatch('AUTH_REQUEST', { email, password })
        .then(() => {
          this.$router.push('/manage')
        })
        .catch((e) => {
          alert(e)
        })
    }
  }
  
}
</script>

<style scoped>

@media screen and (min-width: 1087px) {

  #login {
    margin-top: 100px;
  }

}
</style>

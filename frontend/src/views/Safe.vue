<template>
  <v-container>
    <header>
      <h1 class="title">Dashboard</h1>
      <v-btn class="logout" @click="logOut">Log-out</v-btn>
    </header>
    <section>

    </section>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'panel',
  data () {
    return { }
  },
  beforeCreate: function () {
    if (!this.$session.exists()) {
      this.$router.push({name: "Login"})
    }
  },
  created () {

    console.log(this.$session.get("token"))
    axios.get(`${this.$store.state.HOST}/api/dashboard/check_token/`, 
    {
      // headers: {
      //   "Content-type": "application/json",
      //   "Authorization": this.$store.state.usertoken,
      //   // "X-CSRFToken": payload.csrftoken,
      // }
      params:{
        token: this.$session.get("token")
      }
    }).then( res => {
      console.log(res.data)
    })
  },
  methods: {
    logOut: function () {
      this.$session.destroy()
      this.$router.push({name: "Login"})
    }
  }
}
</script>
  
<style scoped>
  .title {
    display: inline;
  }

  .logout {
    display: inline;
    float: right;
  }


</style>
<template>
  <v-app :dark="true">
    <Nav />
    <v-main>
      <router-view class="animated fadeIn"></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Nav from "./components/layouts/Nav";
import axios from "axios";
export default {
  name: "App",
  components: {
    Nav
  },
  data: () => ({
    //
  }),
  created() {
    this.generateWeekDates()
  },
  methods: {
    scrollTopAnimation() {
      let scrollValue = document.documentElement.scrollTop;
      while (scrollValue > 0) {
        document.documentElement.scrollTop--;
      }
    },

    async generateWeekDates() {
      let self = this;
      await axios
        .post(
          `${self.$store.state.HOST}/api/dashboard/generate_week_dates/`,
          {
            headers: {
              Accept: "application/json",
              "Content-type": "application/json"
              //"Authorization: token ${payload.auth},
              //"X-CSRFToken": payload.csrftoken,
            }
          }
        )
        .then(res => {
          console.log(res.data);
        });
    },
  }
};
</script>

<style>
/* @import url("https://fonts.googleapis.com/css?family=Amita");
@import url("https://fonts.googleapis.com/css?family=Arbutus+Slab"); */
html,
body {
  width: 100%;
  margin: 0px;
  padding: 0px;
  font-family: "Arbutus Slab", Helvetica, Arial, sans-serif;
}
#app {
  /* scroll-behavior: smooth; */
  font-family: "Arbutus Slab", Helvetica, Arial, sans-serif;
  margin: 0px;
  padding: 0px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  /* overflow-x: hidden; */
}
</style>

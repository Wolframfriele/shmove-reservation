<template>
<<<<<<< HEAD
  <v-app :dark="true">
=======
  <v-app :dark='true'>
>>>>>>> Calender v01
    <Nav />
    <v-main>
      <router-view class="animated fadeIn"></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Nav from "./components/layouts/Nav";
export default {
  name: "App",
  components: {
    Nav
  },
  data: () => ({
    //
  }),
  created() {},
  methods: {
    scrollTopAnimation() {
      let scrollValue = document.documentElement.scrollTop;
      while (scrollValue > 0) {
        document.documentElement.scrollTop--;
      }
    }
  }
};
</script>

<style>
/* @import url("https://fonts.googleapis.com/css?family=Amita");
@import url("https://fonts.googleapis.com/css?family=Arbutus+Slab"); */
html,
body {
  scroll-behavior: smooth;
  overflow-x: hidden;
  overflow-y: hidden;
  width: 100%;
  margin: 0px;
  padding: 0px;
<<<<<<< HEAD
  font-family: "Arbutus Slab", Helvetica, Arial, sans-serif;
}
=======
  font-family: "Arbutus Slab", Helvetica, Arial, sans-serif;}
>>>>>>> Calender v01
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

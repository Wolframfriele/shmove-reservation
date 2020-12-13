<template>
<<<<<<< HEAD
  <v-app :dark='true'>
=======
<<<<<<< HEAD
  <v-app :dark="true">
=======
  <v-app :dark='true'>
>>>>>>> 6d2b6ad... frontend merged
>>>>>>> 3327489e70c390d7285e91d02e4be219f984bf3a
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
  font-family: "Arbutus Slab", Helvetica, Arial, sans-serif;}
=======
<<<<<<< HEAD
  font-family: "Arbutus Slab", Helvetica, Arial, sans-serif;
}
=======
  font-family: "Arbutus Slab", Helvetica, Arial, sans-serif;}
>>>>>>> 6d2b6ad... frontend merged
>>>>>>> 3327489e70c390d7285e91d02e4be219f984bf3a
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

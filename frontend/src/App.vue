<template>
  <v-app>
    <Nav />
    <v-content>
      <router-view class="animated fadeIn"></router-view>
    </v-content>
  </v-app>
</template>

<script>
import Nav from "./components/layouts/Nav";
export default {
  name: "App",
  components: {
    Nav,
  },
  data: () => ({
    //
  }),
  created() {
  
  },
  methods: {
    scrollTopAnimation() {
      let scrollValue = document.documentElement.scrollTop;
      while (scrollValue > 0) {
        document.documentElement.scrollTop--;
      }
    },
  },
};
</script>

<style>
/* @import url("https://fonts.googleapis.com/css?family=Amita");
@import url("https://fonts.googleapis.com/css?family=Arbutus+Slab"); */
html,
body {
  scroll-behavior: smooth;
  overflow-x: hidden;
  width: 100%;
  margin: 0px;
  padding: 0px;
  font-family: "Arbutus Slab", Helvetica, Arial, sans-serif;
  background-color: #f5fffa;
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
  background-color: #fffafa;
  /* overflow-x: hidden; */
}
</style>
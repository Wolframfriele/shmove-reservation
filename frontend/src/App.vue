<template>
  <v-app >
    <v-main>
      <router-view class="animated fadeIn"></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  components: {
  },
  data: () => ({
    //
  }),
  methods: {
    scrollTopAnimation() {
      let scrollValue = document.documentElement.scrollTop;
      while (scrollValue > 0) {
        document.documentElement.scrollTop--;
      }
    },
    
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@600&display=swap');
html,
body {
  width: 100%;
  margin: 0px;
  padding: 0px;
  font-family: 'Open Sans', Helvetica, Arial, sans-serif;
}

::-webkit-scrollbar {
  width: 0;
}
#app {
  /* scroll-behavior: smooth; */
  font-family: 'Open Sans', Helvetica, Arial, sans-serif;
  margin: 0px;
  padding: 0px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  /* overflow-x: hidden; */
}

.scroll-hide {
  overflow: auto;
  /* this will hide the scrollbar in mozilla based browsers */
  overflow: -moz-scrollbars-none;
  /* this will hide the scrollbar in internet explorers */
  -ms-overflow-style: none;
}

/* this will hide the scrollbar in webkit based browsers - safari, chrome, etc */
.scroll-hide ::-webkit-scrollbar { 
  width: 0 !important;
  display: none; 
}

</style>

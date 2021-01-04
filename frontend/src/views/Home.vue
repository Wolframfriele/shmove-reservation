<template>
  <div class="home">
    <h1 class="display-3 animated bounceInUp font-weight-bold">
      Welkom SHMOVERS
    </h1>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Home",
  components: {
    
  },

  created(){
  },

  methods:{
    getUser(){
      let self = this;
      self.$store.dispatch("getUser", {
        url: "test/get_user",
        params: { user_id: 1 },
        callback: function(data) {
          console.log(JSON.parse(data));
        },
      });
    }
  }
};
</script>

<style scoped>
.home {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

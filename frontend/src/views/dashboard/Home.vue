<template>
    <Calendar/>
</template>

<script>
// import axios from 'axios';
import Calendar from "../../components/dashboard/Calendar";
export default {
  data: () => ({

  }),

  components:{
    Calendar:Calendar
  },

  created() {
  },

  mounted() {
  },
  methods: {

  },
}
</script>

<style scoped>
.home-core{
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
  height: auto;
  border: 1px solid red;
}
</style>
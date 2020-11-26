<template>
    <v-main>
      <h1 class="display-1">Afspraak Maken:</h1>
      <TijdKiezen class="calender"/>
    </v-main>
</template>

<script>
import TijdKiezen from '../components/TijdKiezen.vue'
export default {
  components: {
    TijdKiezen
  } 
}
</script>

<style scoped>
  h1 {
    text-align: center;
  }

  .calender {
    width: 90%;
    margin: auto;
    overflow: hidden;
  }
</style>

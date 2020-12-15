<template>
  <v-main>
    <h1 class="display-1">Afspraak is geboekt!</h1>
    <BevestigDetails class="form" />
    <!-- <div class="text-center">
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="primary">mdi-circle</v-icon>
    </div> -->
  </v-main>
</template>

<script>
import BevestigDetails from "../components/BevestigDetails.vue";
export default {
  components: {
    BevestigDetails
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin: 2em 1em 0em 0em;
  color: #c49760;
  font-size: .5em;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.form {
  width: 500px;
  margin: 2em auto;
}

.text-center {
  margin: 1em 1em 1em 1em;
}
</style>

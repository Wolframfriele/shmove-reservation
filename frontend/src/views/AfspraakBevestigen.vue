<template>
  <div>
    <h1 class="display-1">Afspraak Bevestigen:</h1>
    <FormBevestig class="form" />
    <!-- <div class="text-center">
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="grey">mdi-circle-slice-8</v-icon>
    </div> -->
  </div>
</template>

<script>
import FormBevestig from "../components/FormBevestig.vue";
export default {
  components: {
    FormBevestig
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin: 0em 1em 1em 0;
  color: #c49760;
  font-size: .5em;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.form {
  width: 500px;
  margin: auto;
}

.text-center {
  margin: 0em 1em 1em 0em;
}
</style>

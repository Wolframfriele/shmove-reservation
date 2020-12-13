<template>
  <v-main>
    <h1 class="display-1">Afspraak Bevestigen:</h1>
    <FormBevestig class="form" />
    <!-- <div class="text-center">
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="grey">mdi-circle-slice-8</v-icon>
    </div> -->
  </v-main>
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
  margin: 1em 1em 2em 1em;
}

.form {
  width: 500px;
  margin: auto;
}

.text-center {
  margin: 1em 1em 1em 1em;
}
</style>

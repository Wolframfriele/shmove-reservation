<template>
  <v-main>
    <h1 class="display-1">Afspraak Bevestigen:</h1>
    <FormBevestig class="form" />
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
  margin: 1em 1em 3em 1em;
}

.form {
  width: 500px;
  margin: auto;
}
</style>

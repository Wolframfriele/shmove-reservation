<template>
  <v-main>
    <h1 class="display-1">Afspraak is geboekt!</h1>
    <BevestigDetails class="form" />
    <AccountMaken class="form" />
  </v-main>
</template>

<script>
import AccountMaken from "../components/AccountMaken.vue";
import BevestigDetails from "../components/BevestigDetails.vue";
export default {
  components: {
    AccountMaken,
    BevestigDetails
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
  margin: 2em auto;
}
</style>

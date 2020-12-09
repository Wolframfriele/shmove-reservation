<template>
  <v-main>
    <h1 class="display-1">Afspraak is geboekt!</h1>
<<<<<<< HEAD
    <div class="text-center">
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="primary">mdi-circle</v-icon>
    </div>
    <BevestigDetails class="form" />
=======
    <BevestigDetails class="form"/>
    <AccountMaken class="form"/>
>>>>>>> 6d2b6ad... frontend merged
  </v-main>
</template>

<script>
<<<<<<< HEAD
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
  margin: 1em 1em 3em 1em;
}

.form {
  width: 500px;
  margin: 2em auto;
}

.text-center {
  margin: 1em 1em 1em 1em;
}
</style>
=======
import AccountMaken from '../components/AccountMaken.vue'
import BevestigDetails from '../components/BevestigDetails.vue'
export default {
  components: {
    AccountMaken,
    BevestigDetails
  }
}
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
>>>>>>> 6d2b6ad... frontend merged

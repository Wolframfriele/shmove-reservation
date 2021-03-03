<template>
  <v-container class="settingsContainer">
    <h1>Instellingen</h1>
    <Treatments />
    <Openingtimes />
  </v-container>
</template>

<script>
import Treatments from "../../components/dashboard/Treatments";
import Openingtimes from "../../components/dashboard/Openingtimes";

export default {
  data: () => ({}),
  components: {
    Treatments,
    Openingtimes
  },
  methods: {}
};
</script>
<style scoped></style>

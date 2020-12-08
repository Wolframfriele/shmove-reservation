<template>
  <v-main>
    <h1 class="display-1">Afspraak Maken:</h1>
    <TypeAfspraak class="type" />
    <TijdKiezen />
  </v-main>
</template>

<script>
import TypeAfspraak from "../components/TypeAfspraak.vue";
import TijdKiezen from "../components/TijdKiezen.vue";

export default {
  components: {
    TypeAfspraak,
    TijdKiezen
  },
  methods: {},
  data() {
    return {};
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin: 1em 1em 1em 1em;
}

.type {
  margin: auto;
  overflow: hidden;
}
</style>

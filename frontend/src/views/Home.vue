<template>
  <div>
    <h1 class="display-1">Afspraak Maken:</h1>
    <TypeAfspraak class="type" />
    <TijdKiezen class="calendar" />
  </div>
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
body {
  overflow-y: hidden;
}

::-webkit-scrollbar {
  width: 0;
}

h1 {
  margin: 0em 0em 0em 0em;
  color: #c49760;
  font-size: 0.5em;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.type {
  width: 300px;
  margin: 0 1em 1em 0em;
  overflow: hidden;
}
.calendar {
  margin: 0;
  height: auto;
  overflow-y: hidden;
}

.text-center {
  margin: 1em 1em 1em 1em;
}
</style>

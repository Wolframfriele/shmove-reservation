<template>
<<<<<<< HEAD
  <v-main>
    <h1 class="display-1">Afspraak Maken:</h1>\
    <div class="text-center">
      <v-icon color="primary">mdi-circle</v-icon>
      <v-icon color="grey">mdi-circle-slice-8</v-icon>
      <v-icon color="grey">mdi-circle-slice-8</v-icon>
    </div>
    <TypeAfspraak class="type" />
    <TijdKiezen class="calendar" />
  </v-main>
</template>

<script>
import TypeAfspraak from "../components/TypeAfspraak.vue";
import TijdKiezen from "../components/TijdKiezen.vue";
=======
    <v-main>
      <h1 class="display-1">Afspraak Maken:</h1>
      <TypeAfspraak class="type" />
      <TijdKiezen />
    </v-main>
</template>

<script>
import TypeAfspraak from '../components/TypeAfspraak.vue'
import TijdKiezen from '../components/TijdKiezen.vue'
>>>>>>> 6d2b6ad... frontend merged

export default {
  components: {
    TypeAfspraak,
    TijdKiezen
  },
<<<<<<< HEAD
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
  width: 300px;
  margin: auto;
  overflow: hidden;
}
.calendar {
  margin: 0;
}

.text-center {
  margin: 1em 1em 1em 1em;
}
</style>
=======
  methods: {
    
  },
  data() {
    return {
      
    }
  },
}
</script>

<style scoped>
  h1 {
    text-align: center;
    margin: 1em 1em 1em 1em;
  }

  .type {
    width: 300px;
    margin: auto;
    overflow: hidden;
  }
</style>
>>>>>>> 6d2b6ad... frontend merged

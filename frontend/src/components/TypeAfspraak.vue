<template>
  <v-container fluid>
    <h2>Type Behandeling:</h2>
    <v-checkbox
      input-value="true"
      label="Knippen"
      value
    ></v-checkbox>
    <v-checkbox
      input-value="false"
      label="verven"
      value
    ></v-checkbox>
    <h2>Haarlengte:</h2>
    <v-radio-group v-model="haarLengte">
      <v-radio
        key="1"
        label="Kort"
        value="1"
      ></v-radio>
      <v-radio
        key="2"
        label="Halflang"
        value="2"
      ></v-radio>
      <v-radio
        key="3"
        label="Lang"
        value="3"
      ></v-radio>
    </v-radio-group>
    <h2>Keuze Stylist:</h2>
    <v-radio-group v-model="stylistkeuze">
      <v-radio
        key="1"
        label="Geen Voorkeur"
        value="1"
      ></v-radio>
      <v-radio
        key="2"
        label="Shane"
        value="2"
      ></v-radio>
      <v-radio
        key="3"
        label="Declan"
        value="3"
      ></v-radio>
    </v-radio-group>
  </v-container>
</template>

<script>
  export default {
    data () {
      return {
        haarLengte: 1,
        stylistkeuze: 1,
      }
    },
  }
</script>
<template>
  <div>
    <p>
      Er is {{ this.$route.params.time }} voor je gereserveerd! Je hebt ook
      een bevestigings mail ontvangen. Hier staat meer informatie over annuleren
      in.
    </p>
    <!-- <v-btn color="secondary" elevation="2" large>Voeg toe aan agenda</v-btn> -->
    <p>
      IN-KI Shiatsu Delft werkt in Corona tijd volgens de richtlijnen van het
      RIVM.
    </p>
  </div>
</template>

<script>
export default {
  mounted() {}
};
</script>

<style scoped>
p {
  margin: 1em 0;
}
</style>

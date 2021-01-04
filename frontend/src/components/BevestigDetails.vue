<template>
  <div>
    <p>
      Er is om {{ this.$route.params.time }} voor je gereserveerd! Je hebt ook een bevestigings mail ontvangen. Hier staat meer informatie over anuleren in.
    </p>
    <v-btn color="secondary" elevation="2" large>Voeg toe aan agenda</v-btn>
    <p>
      Vanwege covid-19 zijn er nog een aantal dingen om rekening mee te houden.
    </p>
  </div>
</template>

<script>
export default {
  mounted() {
    console.log(this.$route.params.time)
  }
}
</script>

<style scoped>
p {
  margin: 1em 0;
}
</style>

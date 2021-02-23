<template>
  <v-card>
    <v-toolbar color="indigo lighten-1" dark>
      <v-toolbar-title>Test Modal</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <p>Modal is opened, amazing!</p>
    <v-card-actions>
        <v-btn text color="secondary" @click="planVacationModal = false">
          Terug
        </v-btn>
      </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data: () => ({
     
  })
}
</script>

<style scoped>
p {
  margin: 10px;
}
</style>
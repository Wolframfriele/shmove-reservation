<template>
  <v-card
    color="grey lighten-4"
    min-width="350px"
    flat
  >
    <v-toolbar :color="selectedEvent.color">
      <v-toolbar-title v-html="selectedEvent.name" class="text--white"></v-toolbar-title>      
    </v-toolbar>
    <v-card-text>
      <br>

      Dit tijdslot is op de website Geblokkeerd. Dit betekend dat er geen afspraak gepland kan worden.
      
    </v-card-text>
    <v-card-actions>
      <v-btn @click="closeModal" text color="gray">
        Terug
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="cancelAppointment">De-Blokkeer</v-btn>     
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  props: ['selectedEvent'],
  data: () => ({
    
  }),
  methods: {
    cancelAppointment() {
      let body = {
        body: {
          appointment_id: this.selectedEvent.appointment_id
        }
      };
      axios.post(
        'dash_appointments/cancel_appointment/', body,
        {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
      .then(res => {
        if (res.data == 'Success') {
          this.$emit("reloadCalendar")
          this.$emit('closeBlockedModal', true)   
        }
      })
      .catch(e => {
          console.log(e);
      });
    },
    closeModal() {
      this.$emit('closeBlockedModal', true)
    },
  }
}
</script>

<style scoped>

</style>
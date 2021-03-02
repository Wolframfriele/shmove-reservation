<template>
<v-card>
  <v-toolbar dark color="teal">
    <v-card-title>
      <span class="headline">Maak een afspraak</span>
    </v-card-title>
    <v-spacer></v-spacer>
    <v-btn @click="blockAfspraak">Blokkeer Afspraak</v-btn>
  </v-toolbar>
  <v-card-text>
    <br>
    <div class="times">
      <div class="timea">
        <label for="startTime">Begintijd: </label>
        <span id="startTime">{{
          dateToString(selectedOpenEvent.start)
        }}</span>
      </div>
      <div class="timeb">
        <label for="endtime">Eindtijd: </label>
        <span id="endtime">{{
          dateToString(selectedOpenEvent.end)
        }}</span>
      </div>
    </div>
    <label>Kies behandeling</label>
    <v-radio-group
    v-model="select"
    row
    >
      <v-radio v-for="a in allTreatments" :key="a.id"
        :label="a"
        :value="a"
      ></v-radio>
    </v-radio-group>
    <div class="container">
      <v-col cols="12" md="12" class="nopadding">
        <v-text-field
          label="Voornaam"
          required
          dense
          v-model="firstname"
        ></v-text-field>
      </v-col>

      <v-col cols="12" md="12" class="nopadding">
        <v-text-field
          label="Achternaam"
          dense
          v-model="lastname"
        ></v-text-field>
      </v-col>

      <v-col cols="12" md="12" class="nopadding">
        <v-text-field
          label="E-mail"
          dense
          v-model="email"
        ></v-text-field>
      </v-col>

      <v-col cols="12" md="12" class="nopadding">
        <v-text-field
          label="Telefoonnummer"
          dense
          v-model="phonenumber"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="12" class="nopadding">
        <v-textarea
          v-model="reason"
          name="reden"
          label="Reden voor de behandeling"
          value="Beschrijf de situatie van de klant"
        ></v-textarea>
      </v-col>
    </div>
  </v-card-text>
  <v-card-actions>
    <v-btn text color="gray" @click="closeModal">
        Terug
    </v-btn>
    <v-spacer></v-spacer>
    <v-btn @click="sendToBackEnd" color="primary" elevation="2"
      >Voeg afspraak toe
    </v-btn>
  </v-card-actions>
</v-card>
</template>

<script>
import axios from "axios";
import repeatedFunctions from "../../mixins/repeatedFunctions";

export default {
  props: ['selectedOpenEvent'],
  mixins: [repeatedFunctions],
  data: () => ({
    allTreatments: [],
    select: "Shiatsu Therapie",
    firstname: "",
    lastname: "",
    email: "",
    phonenumber: "",
    reason: "",
  }),
  created () {
    this.getTreatments()
  },
  methods: {
    getTreatments() {
      axios
        .get('dashboard/get_treatments/', {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
        .then(res => {
          res.data.forEach(element => {
            this.allTreatments.push(
              element.treatment
            )
          });
        });
    },
    sendToBackEnd() {
      const start = this.parseDate(this.selectedOpenEvent.start);
      const end = this.parseDate(this.selectedOpenEvent.end);
      let body = {
        body: {
          date_booked_start: start,
          date_booked_end: end,
          treatment: this.select,
          reason: this.reason,
          first_name: this.firstname,
          last_name: this.lastname,
          email: this.email,
          phone_number: this.phonenumber
        }
      };
      axios
        .post(
          'dash_appointments/new_appointment/', body ,
          {
            headers: {
              Accept: "application/json",
              "Content-type": "application/json",
              "X-CSRFToken": this.$session.get("token"),
              Authorization: `Token ${this.$session.get("token")}`
            }
          })
        .then(res => {
          //Perform Success Action
          if (res.data.error == "None") {
            this.createEventModal = false;
            this.$emit("reloadCalendar")
            this.$emit('closeNewAppointmentModal', true)
          }
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {
          //Perform action in always
        });
    },
    blockAfspraak () {     
      let body = {
        body: {
          start: this.selectedOpenEvent.start,
          end: this.selectedOpenEvent.end
        }
      };
      axios
        .post(
          'dash_appointments/block_appointment/', body ,
          {
            headers: {
              Accept: "application/json",
              "Content-type": "application/json",
              "X-CSRFToken": this.$session.get("token"),
              Authorization: `Token ${this.$session.get("token")}`
            }
          })
        .then(res => {
          //Perform Success Action
          if (res.data == "blocked") {
            this.createEventModal = false;
            this.$emit("reloadCalendar")
            this.$emit('closeNewAppointmentModal', true)
          }
          
        })
        .catch(error => {
          console.log(error);
        })
    },
    closeModal () {
      this.$emit('closeNewAppointmentModal', true)
    },
  }
}
</script>

<style scoped>
form .container {
  flex-flow: row wrap;
  display: flex;
  padding: 10px 0;
}

form .container .nopadding {
  flex-flow: row wrap;
  display: flex;
  padding: 10px 0;
}
</style>
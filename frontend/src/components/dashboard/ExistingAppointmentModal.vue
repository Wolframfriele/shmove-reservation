<template>
  <v-card
    color="grey lighten-4"
    min-width="350px"
    flat
  >
    <v-toolbar :color="selectedEvent.color">
      <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="showBewerkEventModal != true" @click="bewerkAfspraak">Bewerken</v-btn>
      <v-btn v-if="showBewerkEventModal == true" @click="saveEvent">Opslaan</v-btn>
    </v-toolbar>

    <!-- SHOW EVENT MODAL -->

    <div v-if="showBewerkEventModal != true">
      <v-card-text>
        <br />
        <label for="cstartTime">Begintijd: </label>
        <span id="cstartTime">{{ dateToString(selectedEvent.start) }}</span
        ><br />
        <label for="cendtime">Eindtijd: </label>
        <span id="cendtime">{{ dateToString(selectedEvent.end) }}</span
        ><br />
        <br />
        <div v-if="firstName" class="appointmentInfo">
          <div class="box1">
            <label for="firstname">Voornaam: </label>
          </div>
          <div class="box2">
            <span id="firstname">{{ firstName }}</span>
          </div>
          <br />
        </div>
        <div v-if="lastName" class="appointmentInfo">
          <div class="box1">
            <label for="lastname">Achternaam: </label>
          </div>
          <div class="box2">
            <span id="lastname">{{ lastName }}</span>
          </div>
          <br />
        </div>
        <div v-if="email" class="appointmentInfo">
          <div class="box1">
            <label for="email">Email: </label>
          </div>
          <div class="box2">
            <span id="email">{{ email }}</span>
          </div>
          <br />
        </div>
        <div v-if="phoneNumber" class="appointmentInfo">
          <div class="box1">
            <label for="phone">Telefoon: </label>
          </div>
          <div class="box2">
            <span id="phone">{{ phoneNumber }}</span>
          </div>
          <br />
        </div>
        <div v-if="treatment" class="appointmentInfo">
          <div class="box1">
            <label for="treatments">Behandelingen: </label>
          </div>
          <div class="box2">
            <span id="treatments">{{ treatment }}</span>
          </div>
          <br />
        </div>
        <div v-if="reason" class="appointmentInfo">
          <div class="box1">
            <label for="comments">Opmerkingen: </label>
          </div>
          <div class="box2">
            <span id="comments">{{ reason }} </span>
          </div>
          <br />
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="secondary" @click="closeModal">
          Terug
        </v-btn>        
      </v-card-actions>
    </div>

    <!-- BEWERK EVENT MODAL -->

    <div v-if="showBewerkEventModal == true">
      <v-card-text>
        <!-- Bewerk Tijd -->
        <v-text-field
          label="Begintijd"
          v-model="this.appointmentStart"
        ></v-text-field>

        <v-text-field
          label="Eindtijd"
          v-model="this.appointmentEnd"
        ></v-text-field>
        <!-- Bewerk Reden -->
        <v-textarea
            v-model="this.reason"
            name="reden"
            label="Reden voor de behandeling"
        ></v-textarea>
        <!-- Bewerk Persoonsgegevens -->
        <v-text-field
          label="Voornaam"
          v-model="this.firstName"
        ></v-text-field>
        <v-text-field
          label="Achternaam"
          v-model="this.lastName"
        ></v-text-field>
        <v-text-field
          label="Email"
          v-model="this.email"
        ></v-text-field>
        <v-text-field
          label="Telefoon Nummer"
          v-model="this.phoneNumber"
        ></v-text-field>
        <!-- Bewerk behandeling -->
        <label>Kies behandeling</label>
        <v-radio-group
          :v-model="this.treatment"
          :value="this.treatment"
          row
          >
          <v-radio v-for="a in allTreatments" :key="a.id"
            :label="a"
            :value="a"
          ></v-radio>
        </v-radio-group>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="secondary" @click="closeModal">Terug</v-btn>
        <v-spacer></v-spacer>
        <v-btn color="red" @click="cancelAppointment">Verwijder Afspraak</v-btn>
      </v-card-actions>
      
    </div>
  </v-card>
</template>

<script>
import axios from "axios";
import repeatedFunctions from "../../mixins/repeatedFunctions";

export default {
  props: ['selectedEvent'],
  mixins: [repeatedFunctions],
  data: () => ({
    allTreatments: [],
    selectedTreatment: "",
    showBewerkEventModal: false,
    // Appointment Data
    appointmentDate: "",
    appointmentStart: "",
    appointmentEnd: "",
    CredentialsID: "",
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    treatment: "",
    reason: ""

  }),
  created () {
    this.getTreatments()
    this.getAppointmentInfo(this.selectedEvent.appointment_id)
  },
  methods: {
    getAppointmentInfo(appointmentID) {
      axios
        .get(
          'dash_appointments/get_appointment_data/',
          {
            params: {
              appointment_id: appointmentID
            },
            headers: {
              Accept: "application/json",
              "Content-type": "application/json",
              "X-CSRFToken": this.$session.get("token"),
              Authorization: `Token ${this.$session.get("token")}`
            }
          }
        )
        .then(res => {
          // Needed Information
          this.appointmentDate = JSON.parse(res.data[0].appointment)[0].fields.date
          this.appointmentStart = JSON.parse(res.data[0].time_slice)[0].fields.slice_start
          this.appointmentEnd = JSON.parse(res.data[0].time_slice)[0].fields.slice_end  
          this.credentials = JSON.parse(res.data[0].appointment)[0].fields.credentials
          this.firstName = JSON.parse(res.data[0].customer)[0].fields.first_name
          this.lastName = JSON.parse(res.data[0].customer)[0].fields.last_name
          this.email = JSON.parse(res.data[0].customer)[0].fields.email
          this.phoneNumber = JSON.parse(res.data[0].customer)[0].fields.phone_number
          this.treatment = JSON.parse(res.data[0].treatment)[0].fields.treatment
          this.reason = JSON.parse(res.data[0].appointment)[0].fields.reason
        })
        .catch(e => {
          console.log(e);
        });
    },
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
    closeModal() {
      this.$emit('closeAppointmentModal', true)
      this.showBewerkEventModal = false
    },
    cancelAppointment(appointmentID) {
      let self = this;
      let body = {
        body: {
        appointmentID : appointmentID
        }
      }
      axios.post(
        'dash_appointments/cancel_appointment/', body,
        {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get("token"),
            Authorization: `Token ${self.$session.get("token")}`
          }
        }
      );
    },
    bewerkAfspraak() {
      this.showBewerkEventModal = !this.showBewerkEventModal
    },
    saveEvent() {
      this.showBewerkEventModal = !this.showBewerkEventModal
    },
  }
}
</script>

<style scoped>
.appointmentInfo {
  display: flex;
  justify-content: space-between;
}

.box1,
.box2 {
  width: 50%;
}
</style>
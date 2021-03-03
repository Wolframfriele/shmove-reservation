<template>
  <v-card color="grey lighten-4" min-width="350px" flat>
    <v-toolbar :color="selectedEvent.color">
      <v-toolbar-title
        v-html="selectedEvent.name"
        class="text--white"
      ></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="showBewerkEventModal != true" @click="bewerkAfspraak"
        >Bewerken</v-btn
      >
      <v-btn v-if="showBewerkEventModal == true" @click="saveEvent"
        >Opslaan</v-btn
      >
    </v-toolbar>

    <!-- SHOW EVENT MODAL -->

    <div v-if="showBewerkEventModal != true">
      <v-card-text>
        <br />
        <label for="cstartTime">Datum: </label>
        <span id="cstartTime">{{
          parseDate(this.appointmentDate).slice(0, 10)
        }}</span>
        <br />
        <label for="cstartTime">Begintijd: </label>
        <span id="cstartTime">{{ this.appointmentStart.slice(0, 5) }}</span>
        <br />
        <label for="cendtime">Eindtijd: </label>
        <span id="cendtime">{{ this.appointmentEnd.slice(0, 5) }}</span>
        <br />
        <br />
        <div v-if="firstName" class="appointmentInfo">
          <div class="box1">
            <label for="firstname">Naam: </label>
          </div>
          <div class="box2">
            <span id="firstname">{{ firstName }} {{ lastName }}</span>
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
            <label for="comments">Reden: </label>
          </div>
          <div class="box2">
            <span id="comments">{{ reason }} </span>
          </div>
          <br />
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="gray" @click="closeModal">
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
          v-model="appointmentStart"
        ></v-text-field>

        <v-text-field label="Eindtijd" v-model="appointmentEnd"></v-text-field>
        <!-- Bewerk Reden -->
        <v-textarea
          v-model="reason"
          name="reden"
          label="Reden voor de behandeling"
        ></v-textarea>
        <!-- Bewerk behandeling -->
        <label>Kies behandeling</label>
        <v-radio-group v-model="treatment" :value="treatment" row>
          <v-radio
            v-for="singleTreatment in allTreatments"
            :key="singleTreatment.id"
            :label="singleTreatment"
            :value="singleTreatment"
          ></v-radio>
        </v-radio-group>
        <!-- Bewerk Persoonsgegevens -->
        <v-text-field
          label="Klant Nummer"
          v-model="credential_id"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="gray" @click="closeModal">Terug</v-btn>
        <v-spacer></v-spacer>
        <v-btn color="red" @click="deleteCheck = true" class="white--text"
          >Verwijder Afspraak</v-btn
        >
      </v-card-actions>
      <v-overlay v-model="deleteCheck">
        <v-card min-width="600px">
          <v-card-text>
            <h2>Weet je zeker dat je de afspraak wilt verwijderen?</h2>
          </v-card-text>
          <v-card-text>
            <v-btn text color="gray" @click="deleteCheck = false"
              >Anuleren</v-btn
            >
            <v-btn color="red" @click="cancelAppointment()" class="white--text"
              >Verwijder Afspraak</v-btn
            >
          </v-card-text>
        </v-card>
      </v-overlay>
    </div>
  </v-card>
</template>

<script>
import axios from "axios";
import repeatedFunctions from "../../mixins/repeatedFunctions";

export default {
  props: ["selectedEvent"],
  mixins: [repeatedFunctions],
  data: () => ({
    allTreatments: [],
    selectedTreatment: "",
    showBewerkEventModal: false,
    // Appointment Data
    appointmentDate: "",
    appointmentStart: "",
    appointmentEnd: "",
    credential_id: "",
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    treatment: "",
    reason: "",
    deleteCheck: false,
    newModel: [],
    select: ""
  }),
  created() {
    this.getAppointmentInfo(this.selectedEvent.appointment_id);
    this.getTreatments();
  },
  watch: {
    selectedEvent: function() {
      this.getAppointmentInfo(this.selectedEvent.appointment_id);
    }
  },
  methods: {
    getTreatments() {
      axios
        .get("dashboard/get_treatments/", {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
        .then(res => {
          res.data.forEach(element => {
            this.allTreatments.push(element.treatment);
          });
        });
    },
    getAppointmentInfo(appointmentID) {
      axios
        .get("dash_appointments/get_appointment_data/", {
          params: {
            appointment_id: appointmentID
          },
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
        .then(res => {
          // Needed Information
          this.appointmentDate = res.data[0].date;
          this.appointmentStart = res.data[0].start_time;
          this.appointmentEnd = res.data[0].end_time;
          this.credential_id = res.data[0].credential_id;
          this.firstName = res.data[0].first_name;
          this.lastName = res.data[0].last_name;
          this.email = res.data[0].email;
          this.phoneNumber = res.data[0].phone_number;
          this.treatment = res.data[0].treatment;
          this.reason = res.data[0].reason;
        })
        .catch(e => {
          console.log(e);
        });
    },
    closeModal() {
      this.$emit("closeAppointmentModal", true);
      this.showBewerkEventModal = false;
    },
    cancelAppointment() {
      let body = {
        body: {
          appointment_id: this.selectedEvent.appointment_id
        }
      };
      axios
        .post("dash_appointments/cancel_appointment/", body, {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
        .then(res => {
          if (res.data == "Success") {
            this.$emit("reloadCalendar");
            this.$emit("closeAppointmentModal", true);
            this.showBewerkEventModal = false;
            this.deleteCheck = false;
          }
        })
        .catch(e => {
          console.log(e);
        });
    },
    bewerkAfspraak() {
      this.showBewerkEventModal = !this.showBewerkEventModal;
    },
    saveEvent() {
      let body = {
        body: {
          appointment_id: this.selectedEvent.appointment_id,
          date: this.appointmentDate,
          begin_time: this.appointmentStart,
          end_time: this.appointmentEnd,
          treatment: this.treatment,
          customer_id: this.credential_id,
          reason: this.reason
        }
      };
      axios
        .post("dash_appointments/change_appointment/", body, {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
        .then(res => {
          if (res.data == "SUCCESS") {
            this.$emit("reloadCalendar");
            this.$emit("closeAppointmentModal", true);
            this.showBewerkEventModal = false;
          }
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
};
</script>

<style scoped>
.appointmentInfo {
  display: flex;
  justify-content: space-between;
}

.box1 {
  width: 35%;
}

.box2 {
  width: 65%;
}

.spacer {
  margin: 1em;
  padding: 1em;
}
</style>

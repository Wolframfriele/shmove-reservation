<template>
  <v-container class="holidayContainer">
    <h1>Klanten</h1>
    <v-container class="plannedHolidays">
      <div v-if="klanten.length == 0">
        <v-card>
          <v-toolbar>
            <v-card-title>
              Er zijn nog geen bestaande klanten
            </v-card-title>
          </v-toolbar>
          <v-card-text>
            Als klanten worden toegevoegd kunnen deze hier worden terug
            gevonden.
          </v-card-text>
        </v-card>
      </div>
      <v-card
        min-width="350px"
        v-for="(klant, i) in klanten"
        :key="i"
        @click="openKlantModal(klant)"
        class="customer-card"
      >
        <v-toolbar color="teal">
          <v-card-title class="text--white">
            {{ klant.firstName }} {{ klant.lastName }}
          </v-card-title>
        </v-toolbar>
        <v-card-text>
          <p>Email: {{ klant.email }}</p>
          <p>Telefoonnummer: {{ klant.phoneNumber }}</p>
          <p>Klantnummer: {{ klant.customer_id }}</p>
        </v-card-text>
      </v-card>
    </v-container>
    <v-dialog v-model="showKlantModal" hide-overlay offset-x width="500">
      <EditKlantenModal
        v-bind:selectedKlant="selectedKlant"
        @closeKlantModal="showKlantModal = false"
        @reloadKlanten="getClients"
      />
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";
import EditKlantenModal from "../dashboard/EditKlantModal";

export default {
  data: () => ({
    updatedName: "",
    updatedStartDate: "",
    updatedEndDate: "",
    currency: "€",
    menuOne: "",
    menuTwo: "",
    klanten: [],
    showKlantModal: false,
    selectedKlant: ""
  }),
  created() {
    this.getClients();
  },
  components: {
    EditKlantenModal
  },
  methods: {
    getClients() {
      this.klanten = [];
      axios
        .get("dashboard/get_clients/", {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
        .then(res => {
          res.data.forEach(element => {
            this.klanten.push({
              customer_id: element.customer_id,
              firstName: element.first_name,
              lastName: element.last_name,
              email: element.email,
              phoneNumber: element.phone_number
            });
          });
        });
    },
    openKlantModal(klant) {
      this.selectedKlant = klant;
      this.showKlantModal = true;
    }
  }
};
</script>
<style scoped>
.holidayContainer h1,
.holidayContainer h2 {
  margin-left: 12px;
}
.plannedHolidays {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  margin: 15px;
}
.plannedHolidayContainer {
  margin: 30px;
}
.plannedHolidayContainer:first-child {
  margin-left: 1em;
}
.margin {
  margin: 8px;
}
.plannedHolidayContainer p,
.plannedHolidayContainer h4 {
  margin: 8px;
  text-transform: Capitalize;
}
.newHoliday {
  margin: 1em;
  display: flex;
  flex-flow: column;
  max-width: 300px;
}
h1 {
  margin-bottom: 20px;
}
.holidayContainer.container {
  margin-bottom: 80px;
}
.customer-card {
  margin: 1em;
}
</style>

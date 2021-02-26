<template>
  <v-container class="holidayContainer">
    <h1>Geplande vakanties</h1>
    <v-container class="plannedHolidays">
      <div v-if="planneddays.length == 0">
        <v-card>
          <v-card-toolbar>
            <v-card-title>
              Helaas nog geen vakantie ingepland.
            </v-card-title>
          </v-card-toolbar>     
          <v-card-text>
            <v-icon color="orange lighten-2">mdi-white-balance-sunny</v-icon>
            Tijd om snel wat te plannen! Gebruik daarvoor de zonnentjes in de kalender.
          </v-card-text>
        </v-card>
      </div>
      <div v-for="(days, i) in planneddays" :key="i">
        <div class="plannedHolidayContainer">
          <v-text-field
            class="margin"
            label="Vakantie naam"
            :value="days.name"
            v-model="days.name"
            required
          ></v-text-field>
          <v-text-field
            class="margin"
            label="Begin datum (YYYY-mm-dd)"
            :value="days.start_date"
            v-model="days.start_date"
            required
          ></v-text-field>
          <v-text-field
            class="margin"
            label="Eind datum (YYYY-mm-dd)"
            :value="days.end_date"
            v-model="days.end_date"
            required
          ></v-text-field>
          <v-btn
            class="ma-2"
            outlined
            color="teal"
            @click="updateVacation(days.id, days.name, days.start_date, days.end_date)"
          >
            Aanpassen
          </v-btn>
          <v-btn
            class="ma-2"
            outlined
            color="red lighten-2"
            @click="deleteVacation(days.id)"
          >
            Verwijderen
          </v-btn>
        </div>
      </div>
    </v-container>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    updatedName: "",
    updatedStartDate: "",
    updatedEndDate: "",
    currency: "€",
    menuOne: "",
    menuTwo: "",
    planneddays: []
  }),
  created() {
    this.getVacations();
    console.log(this.planneddays)
  },
  methods: {
    async getVacations() {
      let self = this;
      await axios
        .get(`${self.$store.state.HOST}/api/dash_appointments/get_vacations/`, {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get("token"),
            Authorization: `Token ${self.$session.get("token")}`
          }
        })
        .then(res => {
          res.data.forEach(element => {
            this.planneddays.push(element);
          });
        });
    },
    updateVacation(id, name, startdate, enddate) {
      let self = this;
      let body = {
        body: {
          id: id,
          name: name,
          start_date: startdate,
          end_date: enddate
        }
      };
      axios
        .post(
          `${self.$store.state.HOST}/api/dash_appointments/change_vacation/`,
          body,
          {
            headers: {
              Accept: "application/json",
              "Content-type": "application/json",
              "X-CSRFToken": self.$session.get("token"),
              Authorization: `Token ${self.$session.get("token")}`
            }
          }
        )
        .then(res => {
          //Perform Success Action
          console.log(res.data);
          window.location.reload();
        })
        .catch(error => {
          console.log(error);
        });
    },
    deleteVacation(id) {
      //Not yet pushed to Yanickhost it seems :(
      let self = this;
      let body = {
        body: {
          id: id
        }
      }
      axios
        .post(`${this.$store.state.HOST}/api/dash_appointments/delete_vacation/`, body, {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get("token"),
            Authorization: `Token ${self.$session.get("token")}`
          }
        })
        .then(res => {
          //Perform Success Action
          console.log(res.data);
          window.location.reload();
        })
        .catch(error => {
          console.log(error);
        });
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
  margin: 0;
}
.plannedHolidayContainer {
  margin: 30px;
}
.plannedHolidayContainer:first-child {
  margin-left: 0;
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
  margin: 0;
  display: flex;
  flex-flow: column;
  max-width: 290px;
}
h1 {
  margin-bottom: 20px;
}
.holidayContainer.container {
  margin-bottom: 80px;
}
</style>

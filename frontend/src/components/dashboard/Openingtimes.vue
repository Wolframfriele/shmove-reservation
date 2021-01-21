<template>
  <v-container>
    <div class="openingHeader">
      <h2>Openingstijden wijzigen</h2>
      <div class="successt" v-if="this.saveSuccess">
        {{ text }}
      </div>
      <div class="errort" v-if="this.saveError">
        {{ text }}
      </div>
    </div>
    <div class="flexbox">
      <v-row v-for="day in days" :key="day.day_id" class="dayrow">
        <h3>{{ day.title }}</h3>
        <div
          class="outerbigbox"
          v-for="(slot, j) in timeslotsFilter(day.day_id)"
          :key="j"
        >
          <div class="bigbox">
            <v-text-field
              class="textfield"
              label="Starttijd"
              :value="slot.start"
              solo
              clearable
            ></v-text-field>
            <v-text-field
              class="textfield"
              label="Eindtijd"
              :value="slot.end"
              solo
              clearable
            ></v-text-field>
            <v-btn
              x-small
              class="mx-2 plus"
              fab
              dark
              color="red lighten-2"
              @click="deleteSlot(slot.slice_id, day.day_id)"
            >
              <v-icon dark>
                mdi-delete
              </v-icon>
            </v-btn>
            <v-btn
              x-small
              class="mx-2 plus"
              fab
              dark
              color="green lighten-2"
              @click="saveSlot(slot.slice_id)"
            >
              <v-icon dark>
                mdi-check
              </v-icon>
            </v-btn>
          </div>
        </div>
        <div class="buttonrow">
          <v-btn
            class="mx-2 plus"
            fab
            dark
            color="indigo lighten-2"
            @click="addSlot(day.day_id)"
          >
            <v-icon dark>
              mdi-plus
            </v-icon>
          </v-btn>
        </div>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    currency: "€",
    thisday: "",
    saveSuccess: false,
    saveError: false,
    text: "",
    sleep: "",
    days: [
      {
        day_id: "0",
        title: "Maandag"
      },
      {
        day_id: "1",
        title: "Dinsdag"
      },
      {
        day_id: "2",
        title: "Woensdag"
      },
      {
        day_id: "3",
        title: "Donderdag"
      },
      {
        day_id: "4",
        title: "Vrijdag"
      },
      {
        day_id: "5",
        title: "Zaterdag"
      },
      {
        day_id: "6",
        title: "Zondag"
      }
    ],
    timeslots: []
  }),
  created() {
    this.getSlices();
  },
  computed: {},
  methods: {
    async getSlices() {
      let self = this;
      await axios
        .get(`${self.$store.state.HOST}/api/dashboard/get_timeslices/`, {
headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get('token'),
             Authorization: `Token ${self.$session.get('token')}`,
          }
        })
        .then(slices => {
          this.events = [];
          // console.log(res.data);
          slices.data.forEach(slice => {
            self.timeslots.push({
              start: slice.start,
              end: slice.end,
              day_id: slice.day_id,
              slice_id: slice.slice_id
            });
          });
        })
        .catch(e => {
          console.log(e);
        });
    },
    timeslotsFilter(id) {
      let scoped = this.timeslots.filter(item => {
        return item.day_id == id;
      });
      return scoped;
    },
    addSlot(index) {
      this.timeslots.push({
        start: "",
        end: "",
        day_id: index,
        slice_id: 1
      });
    },
    saveSlot() {
      //http://django.yanickhost.ga:8085/api/dashboard/update_timeslices/
      //http://django.yanickhost.ga:8085/api/dashboard/add_time_slices/
      let body = {
        day_id: this.day_id,
        begin_time: this.start,
        end_time: this.end,
        slice_id: this.slice_id
      };

      let self = this;
      axios
        .put(`${self.$store.state.HOST}/api/dashboard/update_timeslices/`, {
          body: body,
headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get('token'),
             Authorization: `Token ${self.$session.get('token')}`,
          }
        })
        .then(res => {
          //Perform Success Action
          console.log(res.status);
          this.saveSucces = true;
          this.text = "Tijden succesvol aangepast!";
          this.getSlices();
          setTimeout(() => {
            this.saveSucces = false;
          }, 5000);
        })
        .catch(error => {
          console.log(error);
          this.saveError = true;
          this.text = "Er is iets fout gegaan bij het opslaan van de tijden!";
          setTimeout(() => {
            this.saveError = false;
          }, 5000);
        });
    },
    deleteSlot(slice_id, day_id) {
      let self = this
      axios
        .delete(`${self.$store.state.HOST}/api/dashboard/remove_timeslices/`, {
          params: {
            slice_id: slice_id,
            day_id: day_id
          },
headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get('token'),
             Authorization: `Token ${self.$session.get('token')}`,
          }
        })
        .then(res => {
          //Perform Success Action
          console.log(res.data);
          // this.getSlices();
        })
        .catch(error => {
          console.log(error);
        });
      //http://django.yanickhost.ga:8085/api/dashboard/remove_timeslices/
      //this.timeslots.splice(slice_id, day_id);
    }
  }
};
</script>
<style scoped>
.test {
  display: none;
  margin-left: 10px;
}

.outerbigbox:empty {
  display: none;
}

h2 {
  margin-bottom: 20px;
}

.outerbigbox {
  width: 100%;
}

.flexbox {
  display: flex;
  flex-flow: row wrap;
  align-items: baseline;
}

.dayrow {
  justify-content: center;
  width: 30%;
  min-width: 400px;
  background-color: #f3f3f399;
  border: 1px solid #ececec;
  border-radius: 15px;
  margin: 20px;
}

.dayrow h3 {
  margin: 20px;
  font-size: 18px;
  width: 100%;
  text-align: center;
}
.openingHeader {
  text-align: center;
}
.successt {
  color: green;
  margin-bottom: 10px;
}
.errort {
  color: red;
  margin-bottom: 10px;
}
.buttonrow {
  margin-bottom: 15px;
}

.bigbox {
  display: flex;
  justify-content: center;
  align-items: baseline;
}

.textfieldContainer {
  display: flex;
  flex-flow: row wrap;
  position: relative;
  max-width: 80%;
}

.textfieldContainer:hover .test {
  display: block;
}

.textfieldContainer div {
  display: flex;
  flex-flow: row wrap;
}

.textfield {
  margin: 0 10px;
  max-width: 200px;
}
</style>

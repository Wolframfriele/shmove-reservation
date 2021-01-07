<template>
  <v-container>
    <h2>Openingstijden wijzigen</h2>
    <div class="flexbox">
      <v-row v-for="day in days" :key="day.day_id" class="dayrow">
        <h3>{{ day.title }}</h3>
        <div
          class="outerbigbox"
          v-for="(slot, slice_id) in timeslots"
          :key="slot.day_id"
        >
          <div class="bigbox" v-if="day.day_id == slot.day_id">
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
              color="red"
              @click="deleteSlot(slice_id)"
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
              color="green"
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
            color="indigo"
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
            "Content-type": "application/json"
            //"Authorization: token ${payload.auth},
            //"X-CSRFToken": payload.csrftoken,
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
    addSlot(index) {
      this.timeslots.push({
        start: "",
        end: "",
        day_id: index
      });
    },
    saveSlot() {
      //http://django.yanickhost.ga:8085/api/dashboard/update_timeslices/
      //http://django.yanickhost.ga:8085/api/dashboard/add_time_slices/
      let body = {
        day_id: this.day_id,
        start: this.start,
        end: this.end,
        slice_id: this.slice_id
      };

      let self = this;
      axios
        .put(`${self.$store.state.HOST}/api/dashboard/update_timeslices`, {
          body: body,
          headers: {
            Accept: "application/json",
            "Content-type": "application/json"
            //"Authorization: token ${payload.auth},
            //"X-CSRFToken": payload.csrftoken,
          }
        })
        .then(res => {
          //Perform Success Action
          console.log(res.data);
          this.getSlices();
        })
        .catch(error => {
          console.log(error);
        });
    },
    deleteSlot(slice_id) {
      //http://django.yanickhost.ga:8085/api/dashboard/remove_timeslices/
      this.timeslots.splice(slice_id, 1);
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
  max-width: 30%;
  background-color: #f3f3f399;
  border-radius: 15px;
  margin: 20px;
}

.dayrow h3 {
  margin: 20px;
  font-size: 18px;
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

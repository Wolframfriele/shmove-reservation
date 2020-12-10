<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="64">
        <v-toolbar flat>
          <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
            Today
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="prev">
            <v-icon small>
              mdi-chevron-left
            </v-icon>
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="next">
            <v-icon small>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
          <v-spacer> </v-spacer>
          <v-toolbar-title>
            Kies een afspraak:
          </v-toolbar-title>
        </v-toolbar>
      </v-sheet>
      <v-sheet>
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
<<<<<<< HEAD
          :event-color="eventColor"
=======
          :event-color="getEventColor"
>>>>>>> 82e04abfd8857c02b1b0c9262fb8316d2c76148a
          :type="type"
          :weekdays="weekdays"
          :first-interval="firstinterval"
          :interval-count="intervalcount"
          :interval-format="intervalFormat"
          :locale="locale"
          @click:event="bevestigAfspraak"
        ></v-calendar>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import { bus } from '../main'
import axios from "axios";

export default {
  data: () => ({
    focus: "",
    type: "week",
    weekdays: [1, 2, 3, 4, 5, 6, 0],
    firstinterval: "9",
    intervalcount: "11",
    locale: "nl",
    eventColor:  ['primary', 'red'],
    treatment: [],
    events: []
  }),
  async created() {
    try {
      // let self = this;
      // const res = await axios.get('https://run.mocky.io/v3/b0538f87-56ff-4b09-b1ed-537e815507c2')
      // console.log(res.data.open);
      // res.data.open.forEach(element => {
      //   this.events.push({
      //     name: "Vrije Afspraak",
      //     start: element.start,
      //     end: element.end,
      //     timed: true
      //   })
      // });

      await this.getFreePlaces();

    } catch (e) {
      console.error(e);
    }
    bus.$on('changeTreatment', (data) => {
      this.treatment = data;
    })
  },
  mounted() {
    this.$refs.calendar.checkChange();
  },
  methods: {
    setToday() {
      this.focus = "";
    },
    prev() {
      this.$refs.calendar.prev();
    },
    next() {
      this.$refs.calendar.next();
    },
    parseDate(date){
      // parse date time to dd-mm-yyy h:m:s
      return new Date(date).toLocaleString();
    },
    getEventColor (event) {
        return event.color
    },
    // updateRange ({ start, end }) {

    // },
    intervalFormat(interval) {
      return interval.time;
    },
    bevestigAfspraak({ event }) {
      this.$router.push({name: "AfspraakBevestigen", params: {start: this.parseDate(event.start), end: this.parseDate(event.end), treatment: this.treatment}});
    },
    getFreePlaces(){
      let self = this;
      axios.get(`${self.$store.state.HOST}/api/appointments/get_free_places/`,
      {}
      ).then(res => {
        console.log(res.data);
        res.data.forEach(times => {
          self.events.push({
            name: times.taked ? "Bezet" : "Vrije Afspraak",
            start: times.start,
            end: times.end,
            color: times.taked ? self.eventColor[1] : self.eventColor[0],
            timed: true
          })
        });
      }).catch(e => {
        console.log(e)
      })
    }
  }
};
</script>

<style scoped>
.v-calendar-daily__scroll-area {
  overflow: hidden;
}
</style>

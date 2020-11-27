<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="64">
<<<<<<< HEAD
        <v-toolbar flat>
          <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
            Today
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="prev">
=======
        <v-toolbar
          flat
        >
          <v-btn
            outlined
            class="mr-4"
            color="grey darken-2"
            @click="setToday"
          >
            Today
          </v-btn>
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="prev"
          >
>>>>>>> Calender v01
            <v-icon small>
              mdi-chevron-left
            </v-icon>
          </v-btn>
<<<<<<< HEAD
          <v-btn fab text small color="grey darken-2" @click="next">
=======
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="next"
          >
>>>>>>> Calender v01
            <v-icon small>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
<<<<<<< HEAD
          <v-spacer> </v-spacer>
=======
          <v-spacer>
          </v-spacer>
>>>>>>> Calender v01
          <v-toolbar-title>
            Kies een afspraak:
          </v-toolbar-title>
        </v-toolbar>
      </v-sheet>
<<<<<<< HEAD
<<<<<<< HEAD
      <v-sheet>
=======
      <v-sheet height="600">
>>>>>>> Calender v01
=======
      <v-sheet height="550">
>>>>>>> All reservation steps and call appointments via api
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
<<<<<<< HEAD
<<<<<<< HEAD
          :event-color="eventColor"
=======
          :event-color="getEventColor"
>>>>>>> Calender v01
=======
          :event-color="eventColor"
>>>>>>> All reservation steps and call appointments via api
          :type="type"
          :weekdays="weekdays"
          :first-interval="firstinterval"
          :interval-count="intervalcount"
          :interval-format="intervalFormat"
<<<<<<< HEAD
          :locale="locale"
          @click:event="bevestigAfspraak"
=======
          :locale='locale'
          @click:event="bevestigAfspraak"
<<<<<<< HEAD
          @click:date.stop
          @change="updateRange"
>>>>>>> Calender v01
=======
>>>>>>> All reservation steps and call appointments via api
        ></v-calendar>
      </v-sheet>
    </v-col>
  </v-row>
</template>
<<<<<<< HEAD

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
    eventColor: "primary",
    treatment: [],
    events: []
  }),
  async created() {
    try {
      const res = await axios.get('https://run.mocky.io/v3/b0538f87-56ff-4b09-b1ed-537e815507c2')
      res.data.open.forEach(element => {
        this.events.push({
          name: "Vrije Afspraak",
          start: element.start,
          end: element.end,
          timed: true
        })
      });
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
    // updateRange ({ start, end }) {

    // },
    intervalFormat(interval) {
      return interval.time;
    },
    bevestigAfspraak({ event }) {
      this.$router.push({name: "AfspraakBevestigen", params: {start: event.start, end: event.end, treatment: this.treatment}});
    }
  }
};
</script>

<style scoped>
.v-calendar-daily__scroll-area {
  overflow: hidden;
}
</style>
=======
  
<script>
import axios from 'axios';

export default {
  data: () => ({
    focus: '',
    type: 'week',
    weekdays: [1, 2, 3, 4, 5, 6, 0],
    firstinterval: '9',
    intervalcount: '9',
    locale: 'nl',
    selectedEvent: {},
    eventColor: 'primary',
    events: [],
  }),
  async created() {
    try {
      const res = await axios.get(`https://run.mocky.io/v3/b456ae47-4cfe-438b-8098-cda5ebb8bbf3`)

      this.events = res.data.events;
    } catch(e) {
      console.error(e)
    }
  },
  mounted () {
    this.$refs.calendar.checkChange()
  },
  methods: {
    setToday () {
      this.focus = ''
    },
    prev () {
      this.$refs.calendar.prev()
    },
    next () {
      this.$refs.calendar.next()
    },
    // updateRange ({ start, end }) {
      
    // },
    intervalFormat(interval) {
      return interval.time
    },
    bevestigAfspraak ({ event }) {
      this.selectedEvent = event
      this.$emit('selectie', this.selectedEvent)
      this.$router.push('afspraak-bevestigen')
    },
  },
}
</script>

<style scoped>
  .v-calendar-daily__scroll-area {
    overflow: hidden;
  }

</style>
>>>>>>> Calender v01

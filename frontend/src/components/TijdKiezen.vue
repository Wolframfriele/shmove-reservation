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
>>>>>>> 6d2b6ad... frontend merged
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
>>>>>>> 6d2b6ad... frontend merged
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
>>>>>>> 6d2b6ad... frontend merged
          <v-toolbar-title>
            Kies een afspraak:
          </v-toolbar-title>
        </v-toolbar>
      </v-sheet>
<<<<<<< HEAD
      <v-sheet>
=======
      <v-sheet height="550">
>>>>>>> 6d2b6ad... frontend merged
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
          :event-color="eventColor"
          :type="type"
          :weekdays="weekdays"
          :first-interval="firstinterval"
          :interval-count="intervalcount"
          :interval-format="intervalFormat"
<<<<<<< HEAD
          :locale="locale"
=======
          :locale='locale'
>>>>>>> 6d2b6ad... frontend merged
          @click:event="bevestigAfspraak"
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
    is_user: true,
    is_employee: true,
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
      // const res = await axios.get(`https://run.mocky.io/v3/b456ae47-4cfe-438b-8098-cda5ebb8bbf3`)
      const res = await axios.post(`http://127.0.0.1:8000/api/appointments/get_appointments_barber/`, 
      {body: {
        start_day: "2020-11-23",
        end_day: "2020-11-29",
        employee_id: 3,
        }
      }
      )

      // this.events = res.data.events;
      console.log(res.data);
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
>>>>>>> 6d2b6ad... frontend merged

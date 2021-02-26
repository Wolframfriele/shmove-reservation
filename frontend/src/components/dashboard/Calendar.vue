<template>
  <div>
    <v-row class="fill-height">
      <v-col>
        <v-sheet height="84">
          <v-toolbar flat>
            <v-btn
              outlined
              class="mr-4"
              color="grey darken-2"
              @click="setToday"
            >
              Vandaag
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
            <v-spacer></v-spacer>
            <v-menu bottom right>
              <template v-slot:activator="{ on, attrs }">
                <v-btn outlined color="grey darken-2" v-bind="attrs" v-on="on">
                  <span>{{ typeToLabel[type] }}</span>
                  <v-icon right>
                    mdi-menu-down
                  </v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="type = 'day'">
                  <v-list-item-title>Dag</v-list-item-title>
                </v-list-item>
                <v-list-item @click="type = 'week'">
                  <v-list-item-title>Week</v-list-item-title>
                </v-list-item>
                <v-list-item @click="type = 'month'">
                  <v-list-item-title>Maand</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-toolbar>
        </v-sheet>
        <v-sheet>
          <v-overlay :absolute="absolute" v-if="loaded == false" opacity="0">
            <v-progress-circular
              indeterminate
              :size="70"
              color="primary"
            ></v-progress-circular>
          </v-overlay>
          <v-calendar
            ref="calendar"
            v-model="focus"
            color="primary"
            :first-interval="firstinterval"
            :interval-count="intervalcount"
            :events="events"
            locale="nl"
            :event-color="getEventColor"
            :type="type"
            :event-overlap-mode="mode"
            @click:event="showModal"
            @click:more="viewDay"
            @click:date="viewDay"
            @change="updateRange"
            :weekdays="weekdays"
          >
            <!-- This piece of code adds the vacation button =) -->
            <template v-slot:day-header="{ date, day, present, past }">
              <v-container v-if="!past" class="vacationContainer">
                <v-btn
                  icon
                  depressed
                  color="orange lighten-2"
                  class="vacationButton"
                  title="Start vakantie"
                  @click="showVacationPlanner({ date })"
                >
                  <v-icon>mdi-white-balance-sunny</v-icon>
                </v-btn>
              </v-container>
            </template>
            <!-- ############################################## -->
            <template v-slot:event="{ event, eventParsed }">
              <p class="event-text">{{ event.name }}</p>
              <p class="event-text">
                {{ eventParsed.start.time }} tot {{ eventParsed.end.time }}
              </p>
            </template>
          </v-calendar>
        </v-sheet>
      </v-col>
    </v-row>

    <!-- Modals -->
    <!-- Toon Afspraak Modal-->
    <v-dialog
      v-model="showEventModal"
      width="500"
      height="250"
      hide-overlay
      offset-x
    >
      <ExistingAppointmentModal 
        v-bind:selectedEvent="selectedEvent"
        @closeAppointmentModal="showEventModal = false"
      />
    </v-dialog>
    <!-- Maak Afspraak Modal -->
    <v-dialog
      v-model="createEventModal"
      width="500"
      height="250"
      hide-overlay
      offset-x
    >
      <NewAppointmentModal 
        v-bind:selectedEvent="selectedEvent"
        @closeNewAppointmentModal="createEventModal = false"
      />
    </v-dialog>
    <!-- Plan Vakantie Modal -->
    <v-dialog
      v-model="planVacationModal"
      width="500"
      height="250"
      hide-overlay
      offset-x
    >
      <PlanVacationModal 
        v-bind:vacationStartDate="vacationStartDate"
        @closeVacationModal="planVacationModal = false"
      />
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";
import ExistingAppointmentModal from "../../components/dashboard/ExistingAppointmentModal";
import NewAppointmentModal from "../../components/dashboard/NewAppointmentModal";
import PlanVacationModal from "../../components/dashboard/PlanVacationModal";
import repeatedFunctions from "../../mixins/repeatedFunctions";

export default {
  mixins: [repeatedFunctions],
  data: () => ({
    // Calendar Data
    loaded: false,
    absolute: true,
    focus: "",
    type: "week",
    typeToLabel: {
      month: "Maand",
      week: "Week",
      day: "Dag"
    },
    mode: "column",
    weekdays: [1, 2, 3, 4, 5, 6, 0],
    value: "",
    firstinterval: "9",
    intervalcount: "12",
    locale: "nl",
    events: [],
    // Open Modals
    createEventModal: false,
    showEventModal: false,
    showBewerkEventModal: false,
    planVacationModal: false,

    vacationStartDate: "",
    // Appointment Data 
    select: "",    
    eventColor: ["teal", "primary", "orange lighten-2", "red darken-4", "grey"],
    selectedEvent: {},
    // Functions
    starttime: "",
    endtime: "",
    success: "",
  }),
  components: {
    ExistingAppointmentModal,
    NewAppointmentModal,
    PlanVacationModal,    
  },
  methods: {    
    viewDay({ date }) {
      this.focus = date;
    },
    updateRange({ start, end }) {
      this.getAllEvents(start.date, end.date);
    },
    getAllEvents(start, end) {
      this.loaded = false
      axios
      .get(
        'dash_appointments/get_appointments/',
        {
          params: {
            beginweek: start,
            endweek: end
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
        this.events = [];
        res.data.forEach(entry => {
          if (entry.type == 0) {
            this.events.push({
              name: entry.name,
              start: entry.start,
              end: entry.end,
              appointment_id: entry.appointment_id,
              color: this.eventColor[0],
            });
          } else if (entry.type == 1) {
            this.events.push({
              name: "Vrije Afspraak",
              start: entry.start,
              end: entry.end,
              color: this.eventColor[1]
            });
          } else if (entry.type == 2) {
            this.events.push({
              name: entry.name,
              start: entry.start,
              end: entry.end,
              color: this.eventColor[2]
            });
          } else if (entry.type == 3) {
            this.events.push({
              name: "Geblokkeerd",
              start: entry.start,
              end: entry.end,
              appointment_id: entry.appointment_id,
              color: this.eventColor[3]
            });
          } else if (entry.type == 4) {
            this.events.push({
              name: "Autoblocked",
              start: entry.start,
              end: entry.end,
              color: this.eventColor[4]
            });
          }
        });
        this.loaded = true
      })
      .catch(e => {
        console.log(e);
      });
    },
    showVacationPlanner({ date }) {
      // Clear Dates
      this.vacationStartDate = "";
      this.vacationEndDate = "";
      // Set Dates
      this.vacationStartDate = date;
      this.showEventModal = false
      this.createEventModal = false
      this.planVacationModal = true;
    },    
    showModal({ event }) {
      this.selectedEvent = event
      if (event.color == this.eventColor[0]) {
        if (this.showEventModal == false) {
          setTimeout(() => {
            this.createEventModal = false
            this.planVacationModal = false
            this.showEventModal = true;
          }, 10);
        } else {
          this.planVacationModal = false
          this.createEventModal = false
          this.showEventModal = false;
        }
      } else if (event.color == this.eventColor[1] || this.eventColor[4]) {
        this.planVacationModal = false
        this.showEventModal = false
        this.createEventModal = true;
      }
    },
  }
};
</script>
<style scoped>
#appointmentbtn {
  right: 15px;
  position: absolute;
  bottom: 15px;
}

div.v-calendar-daily__head {
  margin-right: 0;
}

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

.margin {
  margin: 15px;
}

.top15 {
  margin-top: 30px;
}

.times {
  width: 100%;
  display: flex;
  flex-flow: row wrap;
  justify-content: space-between;
}

/** Add Vacation Button Styling **/
.vacationContainer {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
}

.vacationButton {
  position: absolute;
  right: 5px;
  top: 5px;
}

.event-text {
  padding: 5px;
  margin-bottom: 0px !important;
}



/* Bewerk Afspraak */

.hidden {
  display: none;
}
</style>

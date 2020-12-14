<template>
  <div>
    <v-row class="fill-height">
      <v-col>
        <v-sheet height="64">
          <v-toolbar flat>
            <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
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
        <v-sheet height="600">
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
              @click:event="showEvent"
              @click:more="viewDay"
              @click:date="viewDay"
              @change="getAllEvents"
              :weekdays="weekdays"
          ></v-calendar>
          <!--                                          @click:time="createEvent"-->
        </v-sheet>
      </v-col>
    </v-row>
    <v-dialog v-model="showEventModal" width="500" height="250" hide-overlay offset-x>
      <v-card color="grey lighten-4" min-width="350px" flat>
        <v-toolbar :color="selectedEvent.color" dark>
          <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text v-if='$store.state.dashboard.appointmentDataArr != 0'>
          <br/>
          <label for="cstartTime">Begintijd: </label>
          <span id="cstartTime">{{ convertTime(appointmentInfos[0].appointment.date_booked_start) }}</span><br />
          <label for="cendtime">Eindtijd: </label>
          <span id="cendtime">{{ convertTime(appointmentInfos[0].appointment.date_booked_end) }}</span><br />
          <label for="email">Email: </label>
          <span id="email">{{appointmentInfos[0].customer[0].email}}</span><br/>
          <label for="phone">Telefoon: </label>
          <span id="phone">{{appointmentInfos[0].customer[0].phone_number}}</span><br/>
          <label for="treatments">Behandelingen: </label>
          <span id="treatments" >{{appointmentInfos[0].appointment.treatment}}</span><br/>
          <label for="stylist">Stylist: </label>
          <span id="stylist">{{appointmentInfos[0].employee}}</span>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="secondary" @click="showEventModal = false">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="createEventModal" width="500" height="250" hide-overlay offset-x>
      <v-card>
        <v-toolbar dark color="indigo">
          <v-card-title>
            <span class="headline">Maak een afspraak</span>
          </v-card-title>
        </v-toolbar>
        <v-card-text>
          <br/>
          <label>Kies behandeling(en)</label>
          <v-select id="picktreatments" v-model="select" :items="allTreatments" outlined dense multiple
                    :menu-props="{ top: false, offsetY: true }" @change="calculateDuration()"></v-select>
          <div class="times">
            <div class="timea">
              <label for="startTime">Begintijd: </label>
              <span id="startTime">{{ starttime }}</span>
            </div>
            <div class="timeb">
              <label for="endtime">Eindtijd: </label>
              <span id="endtime">{{ endtime }}</span>
            </div>
          </div>
          <br/>
          <!--          <label>Stylist:</label>-->
          <!--          <v-select id="pickstylist" placeholder="Geen voorkeur" :items="stylists" outlined dense-->
          <!--                    :menu-props="{ top: false, offsetY: true }"></v-select>-->
          <label>Klant:</label>
          <v-form>
            <v-container>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field :counter="15" label="Voornaam" required dense v-model="firstname"></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field :counter="15" label="Achternaam" dense v-model="lastname"></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field label="E-mail" dense v-model="email"></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field label="Telefoonnummer" dense v-model="phone"></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-btn v-on:click="sendToBackEnd()" color="accent" elevation="2" block>Voeg afspraak toe</v-btn>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import axios from 'axios';

export default {
  data: () => ({
    focus: '',
    type: 'week',
    typeToLabel: {
      month: 'Maand',
      week: 'Week',
      day: 'Dag'
    },
    mode: 'column',
    weekdays: [1, 2, 3, 4, 5, 6, 0],
    value: '',
    firstinterval: "9",
    intervalcount: "11",
    locale: "nl",
    events: [],
    select: [{text: 'Massage', value: '120'}],
    allTreatments: [],
    eventColor: ['primary', 'red'],
    // stylists: ['Geen voorkeur', 'Gert', 'Truus', 'Piet', 'Julia'],
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    createEventModal: false,
    showEventModal: false,
    tms: '',
    starttime: '',
    endtime: '',
    success: '',
    firstname: '',
    lastname: '',
    email: '',
    phone: '',
  }),

  computed: {
    ...mapGetters({
      appointmentInfos: "dashboard/getAppointments",
    }),
  },

  created() {
    this.getData();
  },

  mounted() {
    this.$refs.calendar.checkChange();
  },

  methods: {
    sendToBackEnd() {
      const start = this.parseDate(this.selectedEvent.start);
      const end = this.parseDate(this.selectedEvent.end);
      let body = {
      customer_id: 0,
      firstname: this.firstname,
      last_name: this.lastname,
      email: this.email,
      phone_number: this.phone,
      start: start,
      end: end,
      treatment: [],
      employee_id: 0,
      }
      let self = this;
      axios.post(`${self.$store.state.HOST}/api/appointments/new_appointment/`, {body: body})
          .then((res) => {
            //Perform Success Action
            console.log(res.data);
            this.createEventModal = false
            this.getAllEvents()
          })
          .catch((error) => {
            console.log(error)
          }).finally(() => {
        //Perform action in always
      });
    },
    viewDay({date}) {
      this.focus = date
      this.type = 'day'
    },
    parseDate(date){
      return new Date(date).toLocaleString();
    },
    setToday() {
      this.focus = ''
    },
    prev() {
      this.$refs.calendar.prev()
    },
    next() {
      this.$refs.calendar.next()
    },
    async getData() {
      let self = this;
      await axios.get('https://my-json-server.typicode.com/liambenschop/school/treatments/', {}
      ).then((response) => {
        response.data.forEach(item => {
          self.allTreatments.push({
            text: item.title,
            value: item.duration
          })
        })
      })
    },
    async getAllEvents() {
      let self = this;
      await axios.get(`${self.$store.state.HOST}/api/appointments/get_free_places/`,
          {}
      ).then(res => {
        this.events = []
        // console.log(res.data);
        res.data.forEach(times => {
          self.events.push({
            name: times.taked ? "Bezet" : "Vrije Afspraak",
            start: times.start,
            appointmentId: times.appointment_id,
            end: times.end,
            color: times.taked ? self.eventColor[1] : self.eventColor[0],
            timed: true
          })
        });
      }).catch(e => {
        console.log(e)
      })
    },

    async getAppointmentInfo(appointmentID){
       let self = this;
      await axios.get(`${self.$store.state.HOST}/api/appointments/get_appointment_data/`,
          {
            params: {
              appointment_id: appointmentID
            }
          }
      ).then(res => {
        console.log(res.data);

        self.$store.getters['dashboard/setAppointments'](res.data)
      }).catch(e => {
        console.log(e)
      })
    },

    showEvent({nativeEvent, event}) {
      let self = this;
      this.selectedEvent = event
      this.selectedElement = nativeEvent.target
      this.starttime = new Date(this.selectedEvent.start)
      this.endtime = new Date(this.selectedEvent.end)
      let startHours = this.starttime.getHours().toString();
      let startMinutes = this.starttime.getMinutes().toString();
      let endHours = this.endtime.getHours().toString();
      let endMinutes = this.endtime.getMinutes().toString();

      this.starttime = startHours.padStart(2, '0') + ':' + startMinutes.padStart(2, '0')
      this.endtime = endHours.padStart(2, '0') + ":" + endMinutes.padStart(2, '0')

      if (this.selectedEvent.color == 'red') {
        // console.log(event)
        self.getAppointmentInfo(event.appointmentId)
        if (this.showEventModal == false) {
          setTimeout(() => {
            this.showEventModal = true
          }, 10)
        } else {
          this.showEventModal = false;
        }
      } else {
        this.createEventModal = true
      }
    },
    getEventColor(event) {
      return event.color
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    calculateDuration(endtime) {
      this.endtime = endtime;
      let sum = 0;
      for (let i = 0; i < this.select.length; i++) {
        sum += (parseFloat(this.select[i]));
      }
      let [hours, minutes] = this.starttime.split(':');
      hours = parseInt(hours);
      minutes = parseInt(minutes);
      minutes += sum;
      this.endtime = (hours * 60) + minutes;     // Convert hours and minutes to time in minutes
      let rounded = Math.round(this.endtime / 15) * 15;
      let rHr = '' + Math.floor(rounded / 60)
      let rMin = '' + rounded % 60
      this.endtime = rHr.padStart(2, '0') + ':' + rMin.padStart(2, '0')
    },
    convertTime(date) {
      const days = [
        'zondag',
        'maandag',
        'dinsdag',
        'woensdag',
        'donderdag',
        'vrijdag',
        'zaterdag'
      ];
      const months = [
        'januari',
        'februari',
        'maart',
        'april',
        'mei',
        'juni',
        'juli',
        'augustus',
        'september',
        'oktober',
        'november',
        'december'
      ];
      const reserverings_tijd = new Date(date).to;

      const dayIndex = reserverings_tijd.getDay();
      const day = days[dayIndex];
      const monthIndex = reserverings_tijd.getMonth();
      const number = reserverings_tijd.getDate();
      const month = months[monthIndex];
      const hours = reserverings_tijd.getHours().toString();
      const minutes = reserverings_tijd.getMinutes().toString();

      return `${day} ${number} ${month} om ${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`;
    },
    // createEvent(tms) {
    //   if (this.createEventModal == false) {
    //     this.tms = tms
    //     //Starttime minutes
    //     let [hours, minutes] = this.tms.time.split(':');
    //     hours = parseInt(hours);
    //     minutes = parseInt(minutes);
    //     this.tms.time = (hours * 60) + minutes;     // Convert hours and minutes to time in minutes
    //     let rounded = Math.round(this.tms.time / 15) * 15;
    //     let rHr = '' + Math.floor(rounded / 60)
    //     let rMin = '' + rounded % 60
    //     this.starttime = rHr.padStart(2, '0') + ':' + rMin.padStart(2, '0')
    //     this.endtime = this.starttime;
    //     //Endtime minutes
    //     let [endHours, endMinutes] = this.endtime.split(':');
    //     endHours = parseInt(endHours);
    //     endMinutes = parseInt(endMinutes);
    //     endMinutes += 30;
    //     this.endtime = (endHours * 60) + endMinutes;
    //     let endRounded = Math.round(this.endtime / 15) * 15;
    //     let endrHr = '' + Math.floor(endRounded / 60)
    //     let endrMin = '' + endRounded % 60
    //     this.endtime = endrHr.padStart(2, '0') + ':' + endrMin.padStart(2, '0')
    //     this.createEventModal = true
    //   } else {
    //     this.createEventModal = false;
    //   }
    // },
  },
}
</script>

<style scoped>
#appointmentbtn {
  right: 15px;
  position: absolute;
  bottom: 15px;
}

form .container {
  padding: 0 !important;
}

.times {
  width: 50%;
  display: flex;
  flex-flow: row wrap;
  justify-content: space-between;
}
</style>
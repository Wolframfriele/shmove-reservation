// import "material-design-icons-iconfont/dist/material-design-icons.css";
// import "@fortawesome/fontawesome-free/css/all.css";
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// import "./registerServiceWorker";
import vuetify from "./plugins/vuetify";
import VAnimateCss from "v-animate-css";
import Vuex from "vuex";
import Axios from "axios";
//Aos imports
import AOS from "aos";
import "aos/dist/aos.css";
import VueSession from "vue-session";

Vue.config.productionTip = false;
Vue.use(VAnimateCss);
Vue.use(Vuex);
Vue.use(VueSession, { persist: true });

Axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
Axios.defaults.xsrfCookieName = "XCSRF-TOKEN";
Axios.defaults.withCredentials = true;
Axios.defaults.baseURL = "https://shiatsudelft.pythonanywhere.com/api/";
// Axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'

Vue.prototype.$axios = Axios;

Vue.config.productionTip = false;

export const bus = new Vue();

new Vue({
  created() {
    AOS.init();
  },
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");

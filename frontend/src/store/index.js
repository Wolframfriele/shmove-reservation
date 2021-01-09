import Vue from "vue";
import Vuex from "vuex";

// import work from "./modules/work";  // store file from modules map import example

import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    HOST:
      // window.location.port != ""
        // ? " http://127.0.0.1:8000"
        // : "django.yanickhost.ga:8085",
       "http://django.yanickhost.ga:8085",
    AUTHENTICATED: undefined,
    usertoken: undefined
  },

  getters: {},

  mutations: {
    splitToArray(state, str) {
      /*
      split a string words in to array
      params:
        str: [str]: [string to split]
      returns: return array
      */
      let arr = str.split(",");
      console.log(arr);
      // return "hallo tehre";
    },

    getAxiosCall(state, payload) {
      /*
                      http get request
                      params:
                          payload: [object]: [data sended with the request]
                  */
      axios
        .get(`${payload.host}/api/${payload.url}/`, {
          params: payload.params
          // headers: {
          //     "X-CSRFToken": payload.csrftoken,
          //     Authorization: `token ${payload.auth}`,
          // },
        })
        .then(response => {
          let res = response.data;
          payload.callback(res);
        })
        .catch(error => {
          console.log(error);
        });
    },

    postAxiosCall(state, payload) {
      /*
           http post request
           params:
               payload: [object]: [data sended with the request]
       */
      axios
        .post(`${payload.host}/api/${payload.url}/`, {
          body: payload.params
          // headers: {
          //     "X-CSRFToken": payload.csrftoken,
          //     Authorization: `token ${payload.auth}`,
          // },
        })
        .then(response => {
          let res = response.data;
          payload.callback(res);
        })
        .catch(error => {
          console.log(error);
        });
    }
  },

  actions: {},

  modules: {}
});

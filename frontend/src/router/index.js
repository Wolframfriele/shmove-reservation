import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
<<<<<<< HEAD
<<<<<<< HEAD
    path: "/afspraak-maken",
    name: "Afspraak Maken",
=======
=======
    path: "/afspraak-maken",
    name: "Afspraak Maken",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AfspraakMaken.vue")
  },
  {
>>>>>>> All reservation steps and call appointments via api
    path: "/afspraak-bevestigen",
    name: "AfspraakBevestigen",
>>>>>>> Calender v01
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
<<<<<<< HEAD
      import(/* webpackChunkName: "about" */ "../views/AfspraakMaken.vue"),
    props: true
  },
  {
    path: "/afspraak-bevestigen",
    name: "AfspraakBevestigen",
=======
      import(/* webpackChunkName: "about" */ "../views/AfspraakBevestigen.vue")
  },
  {
<<<<<<< HEAD
    path: "/afspraak-maken",
    name: "Afspraak Maken",
>>>>>>> Calender v01
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
<<<<<<< HEAD
      import(/* webpackChunkName: "about" */ "../views/AfspraakBevestigen.vue"),
    props: true
  },
  {
=======
>>>>>>> All reservation steps and call appointments via api
    path: "/afspraak-geboekt",
    name: "AfspraakGeboekt",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
<<<<<<< HEAD
      import(/* webpackChunkName: "about" */ "../views/AfspraakGeboekt.vue"),
    props: true
=======
      import(/* webpackChunkName: "about" */ "../views/AfspraakMaken.vue")
>>>>>>> Calender v01
=======
      import(/* webpackChunkName: "about" */ "../views/AfspraakGeboekt.vue")
>>>>>>> All reservation steps and call appointments via api
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;

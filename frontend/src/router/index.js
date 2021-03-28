import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import login from "../views/login.vue";
import register from "../views/register.vue";
import CreateLoan from "../views/CreateLoan.vue";
import CreateFund from "../views/CreateFund.vue";
import CreateFundApp from "../views/CreateFundApp.vue";
import ListFundApps from "../views/ListFundApps.vue";
import UpdateFundApp from "../views/UpdateFundApp.vue";
import CreateLoanApp from "../views/CreateLoanApp.vue";
import ListLoanApps from "../views/ListLoanApps.vue";
import UpdateLoanApp from "../views/UpdateLoanApp.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/register",
    name: "register",
    component: register
  },
  {
    path: "/login",
    name: "login",
    component: login
  },
  {
    path: "/createloan",
    name: "CreateLoan",
    component: CreateLoan
  }, 
  {
    path: "/createfund",
    name: "CreateFund",
    component: CreateFund
  },
  {
    path: "/createfundapp",
    name: "CreateFundApp",
    component: CreateFundApp
  },
  {
    path: "/fundapps",
    name: "ListFundApps",
    component: ListFundApps
  },
  {
    path: "/fundapps/:id",
    name: "UpdateFundApp",
    component: UpdateFundApp
  },
  {
    path: "/createloanapp/",
    name: "CreateLoanApp",
    component: CreateLoanApp
  },
  {
    path: "/loanapps/",
    name: "ListLoanApps",
    component: ListLoanApps
  },
  {
    path: "/loanapps/:id",
    name: "UpdateLoanApp",
    component: UpdateLoanApp
  },
  {
    path :'*',
    component: Home
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;

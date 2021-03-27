<template>
  <div class="home">
    <v-container >
      <v-layout row justify-center>
        <v-flex xs12 md10>
              <h1 class="blue-grey--text">Loans</h1>
              <data-table :data="loans" :headers="loanheaders" :goToLink="/loans/"></data-table>
              <h1 class="blue-grey--text">Loan Funds</h1>
              <data-table :data="loanfunds" :headers="fundheaders" :goToLink="/loanfunds/"></data-table>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import DataTable from '../components/DataTable.vue';

export default {
  name: "Home", 
  components: {
    DataTable
  },
  created() {
    this.getLoans();
    this.getLoanFunds();
  },
  data: () => ({
    loans: [],
    loanfunds: [],
    loanheaders: [],
    fundheaders: [],
    title: 'Loans'
  }),
  methods: {
    //  {
    //         headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},      
    //       }
    getLoans() {
        axios.get('api/loans/')
          .then(resp => {
            // console.log(resp.data);
            this.loanheaders = [
              { text: 'ID', value: 'id' },
              { text: 'Loan type', value: 'loan_fund.fund_type' },
              { text: 'Duration(Yrs)', value: 'duration' },
              { text: 'Interest Rate(%)', value: 'interest_rate' },
              { text: 'Min Amount($)', value: 'min_amount' },
              { text: 'Max Amount($)', value: 'max_amount' },
              // { text: 'Delete', value: 'delete'},
            ]
            // allow delete functionality on loan funds only for Bank Per
            if(localStorage.getItem('user-type') === "Bank Per")
              this.loanheaders.push({ text: 'Delete', value: 'delete'});

            this.loans = resp.data;
            console.log(this.loans);
          })
          .catch(err => {
            console.log(err);
          })  
    },
    getLoanFunds() {
      axios.get('api/loanfunds/')
        .then(resp => {
          console.log(resp.data);
          this.loanfunds = resp.data;
          this.fundheaders = [
            { text: 'ID', value: 'id' },
            { text: 'Loan type', value: 'fund_type' },
            { text: 'Duration(Yrs)', value: 'duration' },
            { text: 'Interest Rate(%)', value: 'interest_rate' },
            { text: 'Min Amount($)', value: 'min_amount' },
            { text: 'Max Amount($)', value: 'max_amount' },
            { text: 'Current Amount($)', value: 'current_amount' },
            // { text: 'Delete', value: 'delete'},   
          ]
          // allow delete functionality on loans only for Bank Per
            if(localStorage.getItem('user-type') === "Bank Per")
              this.fundheaders.push({ text: 'Delete', value: 'delete'});

        })
        .catch(err => {
          console.log(err);
        })  
    },

  }
};
</script>

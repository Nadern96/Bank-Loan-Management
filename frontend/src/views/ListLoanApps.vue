<template>
  <div class="home">
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md10>
              <h1 class="blue-grey--text">Loan Applications</h1>
              <data-table :data="loanapps" :headers="loanheaders" :goToLink="/loanfundapps/"></data-table>
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
  name: "ListLoanApps", 
  components: {
    DataTable
  },
  created() {
    this.getLoanApps();
  },
  data: () => ({
    loanapps: [],
    loanheaders: [],
  }),
  methods: {
    //  {
    //         headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},      
    //       }
    getLoanApps() {
      axios.get('api/loanapps/',
        {
            headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},      
        })
        .then(resp => {
          this.loanapps = resp.data;
          this.loanheaders = [
            { text: 'ID', value: 'id' },
            { text: 'Customer', value: 'customer.username' },
            { text: 'Loan type', value: 'loan.loan_fund.fund_type' },
            { text: 'Duration(Yrs)', value: 'loan.duration' },
            { text: 'Interest Rate(%)', value: 'loan.interest_rate' },
            { text: 'Amount($)', value: 'amount' },
            { text: 'Status', value: 'status' },
            // { text: 'Delete', value: 'delete'},   
          ]
          if(localStorage.getItem('user-type') === "Bank Per")
              this.loanheaders.push({ text: 'Delete', value: 'delete'});

        })
        .catch(err => {
          console.log(err);
        })  
    },

  }
};
</script>

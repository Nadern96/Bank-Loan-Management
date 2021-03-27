<template>
  <div class="home">
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md10>
              <h1 class="blue-grey--text">Loan Fund Applications</h1>
              <data-table :data="loanfunds" :headers="fundheaders" :goToLink="/loanfundapps/"></data-table>
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
  name: "ListFundApps", 
  components: {
    DataTable
  },
  created() {
    this.getLoanFundApps();
  },
  data: () => ({
    loanfunds: [],
    fundheaders: [],
  }),
  methods: {
    //  {
    //         headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},      
    //       }
    getLoanFundApps() {
      axios.get('api/loanfundapps/',
        {
            headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},      
        })
        .then(resp => {
          this.loanfunds = resp.data;
          this.fundheaders = [
            { text: 'ID', value: 'id' },
            { text: 'Provider', value: 'provider.username' },
            { text: 'Loan type', value: 'loan_fund.fund_type' },
            { text: 'Duration(Yrs)', value: 'loan_fund.duration' },
            { text: 'Interest Rate(%)', value: 'loan_fund.interest_rate' },
            { text: 'Amount($)', value: 'amount' },
            { text: 'Status', value: 'status' },
            // { text: 'Delete', value: 'delete'},   
          ]
          // allow delete functionality on loan fund apps only for Bank Per
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

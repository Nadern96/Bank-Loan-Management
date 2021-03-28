<template>
  <div>
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md10>
              <h1 class="blue-grey--text">Loan Fund Applications</h1>
              <data-table :data="loanfunds" 
                          :headers="fundheaders" 
                          :goToLink="/loanfundapps/" 
                          :tableName="'Loan Fund Applications'">
              </data-table>
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
    if(!localStorage.getItem('user-token')){
        this.$router.push('/login');
    }
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
          this.fundheaders = [
            { text: 'ID', value: 'id' },
            { text: 'Provider', value: 'provider' },
            { text: 'Loan type', value: 'fund_type' },
            { text: 'Duration(Yrs)', value: 'duration' },
            { text: 'Interest Rate(%)', value: 'interest_rate' },
            { text: 'Amount($)', value: 'amount' },
            { text: 'Status', value: 'status' },
            // { text: 'Delete', value: 'delete'},   
          ]
          // allow delete functionality on loan fund apps only for Bank Per
          
          for(let i=0; i < resp.data.length; i++){
              let obj = resp.data[i];
              let temp = {
                id:obj.id, 
                provider: obj.provider.username, 
                fund_type: obj.loan_fund.fund_type, 
                duration: obj.loan_fund.duration,
                interest_rate: obj.loan_fund.interest_rate, 
                amount: obj.amount, 
                status: obj.status,
              };
              this.loanfunds.push(temp);
            }

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

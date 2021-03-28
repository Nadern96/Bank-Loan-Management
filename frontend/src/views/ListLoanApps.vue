<template>
  <div>
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md10>
              <h1 class="blue-grey--text">Loan Applications</h1>
              <data-table :data="loanapps" 
                          :headers="loanheaders" 
                          :goToLink="/loanfundapps/" 
                          :tableName="'Loan Applications'">
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
  name: "ListLoanApps", 
  components: {
    DataTable
  },
  created() {
    if(!localStorage.getItem('user-token')){
        this.$router.push('/login');
      }
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
          this.loanheaders = [
            { text: 'ID', value: 'id' },
            { text: 'Customer', value: 'customer' },
            { text: 'Loan type', value: 'fund_type' },
            { text: 'Duration(Yrs)', value: 'duration' },
            { text: 'Interest Rate(%)', value: 'interest_rate' },
            { text: 'Amount($)', value: 'amount' },
            { text: 'Status', value: 'status' },
            // { text: 'Delete', value: 'delete'},   
          ]



            for(let i=0; i < resp.data.length; i++){
              let obj = resp.data[i];
              let temp = {
                id: obj.id, 
                customer: obj.customer.username, 
                fund_type: obj.loan.loan_fund.fund_type, 
                duration: obj.loan.duration,
                interest_rate: obj.loan.interest_rate, 
                amount: obj.amount, 
                status: obj.status,
              };
              this.loanapps.push(temp);
            }

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

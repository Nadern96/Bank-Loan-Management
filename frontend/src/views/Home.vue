<template>
  <div>
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md10>
              <h1 class="blue-grey--text">Loans</h1>
              <data-table :data="loans" 
                          :headers="loanheaders" 
                          :goToLink="/loans/" 
                          :tableName="'Loans'" >
              </data-table>
              <h1 class="blue-grey--text">Loan Funds</h1>
              <data-table :data="loanfunds" 
                          :headers="fundheaders" 
                          :goToLink="/loanfunds/" 
                          :tableName="'Loan Funds'">
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
            this.loanheaders = [
              { text: 'ID', value: 'id' },
              { text: 'Loan type', value: 'fund_type' },
              { text: 'Duration(Yrs)', value: 'duration' },
              { text: 'Interest Rate(%)', value: 'interest_rate' },
              { text: 'Min Amount($)', value: 'min_amount' },
              { text: 'Max Amount($)', value: 'max_amount' },
              // { text: 'Delete', value: 'delete'},
            ]
            // allow delete functionality on loan funds only for Bank Per
            if(localStorage.getItem('user-type') === "Bank Per")
              this.loanheaders.push({ text: 'Delete', value: 'delete'});

            // unpack data into loans to be easily displayed using data-table
            // this.loans = resp.data;
            for(let i=0; i < resp.data.length; i++){
              let obj = resp.data[i];
              let temp = {
                id:obj.id, 
                fund_type: obj.loan_fund.fund_type, 
                duration: obj.duration, 
                interest_rate: obj.interest_rate, 
                min_amount: obj.min_amount, 
                max_amount: obj.max_amount
              };
              this.loans.push(temp);
            }
          })
          .catch(err => {
            console.log(err);
          })  
    },
    getLoanFunds() {
      axios.get('api/loanfunds/')
        .then(resp => {
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

            for(let i=0; i < resp.data.length; i++){
              let obj = resp.data[i];
              let temp = {
                id:obj.id, 
                fund_type: obj.fund_type, 
                duration: obj.duration, 
                interest_rate: obj.interest_rate, 
                min_amount: obj.min_amount, 
                max_amount: obj.max_amount,
                current_amount: obj.current_amount
              };
              this.loanfunds.push(temp);
            }
        })
        .catch(err => {
          console.log(err);
        })  
    },

  }
};
</script>

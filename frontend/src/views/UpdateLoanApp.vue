<template>
  <div class="register">
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md10>
          <v-card>
            <v-card-title>
              <h2 class="blue-grey--text text-center">Loan Fund Application</h2>
            </v-card-title>
            <v-card-text>
              <v-form
                ref="form"
                v-model="valid"
                lazy-validation
                
              >
                <v-text-field
                    class="mt-5"
                  v-model="username"
                  label="username"
                  disabled
                ></v-text-field>

                <v-text-field
                    class="mt-5"
                  v-model="status"
                  label="Status"
                  disabled
                    v-if="disableStatus"
                ></v-text-field>

                <v-select 
                  v-model="status"
                  :items="types"
                  :rules="[v => !!v || 'Item is required']"
                  label="Status"
                  required
                  v-else
                ></v-select>

                
                <v-text-field
                    class="mt-5"
                  v-model="amount"
                  type="number"
                  disabled
                  label="Amount ($)"
                ></v-text-field>

                 <v-text-field
                    class="mt-5"
                  v-model="loan"
                  disabled
                  label="Loan"
                ></v-text-field>
                
                
                <p  class="red--text font-weight-bold">{{response}}</p>
                <v-btn
                    v-if="!disableStatus"
                  :disabled="!valid"
                  color="primary"
                  class="mr-4"
                  mt-5  
                  @click="validate"
                >
                  Submit  
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>

            <div class="mt-5" v-if="disableStatus && status ==='Accepted'">
                <v-btn :disabled="!tableshown" @click="displayAmortizationTable" class='primary'>Show Amortization Table</v-btn>
                <p class="mt-5 red--text font-weight-bold">{{amortizationResp}}</p>

                <data-table :data="amorTable" :headers="amorheaders" :goToLink="/login/"></data-table>

            </div>

        </v-flex>
      </v-layout>
    </v-container>
    
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import axios from 'axios';
import DataTable from '../components/DataTable.vue';

export default {
  name: "UpdateLoanApp",
  components: {
    DataTable
  },
  created() {
      if(!localStorage.getItem('user-token')){
        this.$router.push('/login');
      }
      else if (localStorage.getItem('user-type') == 'PROV')
        this.$router.push('/');
      else if (localStorage.getItem('user-type') == 'CUST')
        this.disableStatus = true;
      this.getLoanApp();
  },
  data: () => ({
      valid: true,
      username: '',
      amount: 0,
      status: '',
        types: [
        'Pending',
        'Rejected',
        'Accepted'
      ],
      loan: '',
      response: '',
      disableStatus: false,
      amortizationResp: '',
      amorTable: [],
      amorheaders: [],
      tableshown: true,
  }),

  methods: {
    getLoanApp() {
        let id = this.$route.params.id;
      axios.get(`/api/loanapps/${id}`, {
          headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
        })
        .then(resp => {
          let data = resp.data;
            this.username = data.customer.username.toUpperCase();
            this.status = data.status;
            this.amount = data.amount;
            this.loan = `${data.loan.id} -  ${data.loan.loan_fund.fund_type} - ${data.loan.duration} years - ${data.loan.interest_rate}%`;

            if (this.status === 'Accepted' && localStorage.getItem('user-type') == 'Bank Per')
                this.disableStatus = true;

        })
        .catch(err => {
          console.log(err);
        })  
    },

    validate () {
        if(this.$refs.form.validate()){
            let id = this.$route.params.id;

            axios.put(`/api/loanapps/${id}/`, {
                    status: this.status             
                },
                {
                    headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
            })
            .then(resp => {
                if (resp.data.error)
                    this.response = resp.data.error;
                else{
                    this.response = 'Succefully updated!'
                    this.disableStatus = true;
                }
            })
            .catch(err => {
                console.log(err);
                this.response = err;
            })  
        }
      },
      displayAmortizationTable() {
          let id = this.$route.params.id;
          axios.get(`/api/loanapps/${id}/amortization/`,{
                headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
            })
            .then(resp => {
                if (resp.data.error){
                    this.amortizationResp = resp.data.error;
                    this.tableshown = true;
                }
                else{
                    this.amorTable = resp.data;
                    this.amorheaders = [
                        { text: 'Period no.', value: 'period' },
                        { text: 'Amount ($)', value: 'amount' },
                        { text: 'Interest Rate(%)', value: 'interest' },
                        { text: 'Principal ($)', value: 'principal' },
                        { text: 'Balance ($)', value: 'balance' },
                    ]
                    this.tableshown = false;
                }
            })
            .catch(err => {
                console.log(err);
                this.response = err;
            })  
      }
  }
};
</script>

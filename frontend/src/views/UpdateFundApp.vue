<template>
  <div class="register">
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md10>
          <v-card>
            <v-card-title>
              <h2 class="blue-grey--text">Loan Fund Appication</h2>
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
                  v-model="loanfund"
                  disabled
                  label="Loan Fund"
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
  name: "UpdateFundApp",
  components: {
    DataTable
  },
  created() {
      if(!localStorage.getItem('user-token')){
        this.$router.push('/login');
      }
      else if (localStorage.getItem('user-type') == 'CUST')
        this.$router.push('/');
      else if (localStorage.getItem('user-type') == 'PROV')
        this.disableStatus = true;
      this.getLoanFundApp();
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
      loanfund: '',
      response: '',
      disableStatus: false,
      amortizationResp: '',
      amorTable: [],
      amorheaders: [],
      tableshown: true,
  }),

  methods: {
    getLoanFundApp() {
        let id = this.$route.params.id;
      axios.get(`/api/loanfundapps/${id}`, {
          headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
        })
        .then(resp => {
          let data = resp.data;
            this.username = data.provider.username.toUpperCase();
            this.status = data.status;
            this.amount = data.amount;
            this.loanfund = `${data.loan_fund.id} -  ${data.loan_fund.fund_type} - ${data.loan_fund.duration} years - ${data.loan_fund.interest_rate}%`;

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

            axios.put(`/api/loanfundapps/${id}/`, {
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
          axios.get(`/api/loanfundapps/${id}/amortization/`,{
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

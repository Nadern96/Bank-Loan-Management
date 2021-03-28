<template>
  <div>
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md6>
          <v-card>
            <v-card-title>
              <h2 class="blue-grey--text">Apply for a Loan</h2>
            </v-card-title>
            <v-card-text>
              <v-form
                ref="form"
                v-model="valid"
                lazy-validation
                
              >
                <v-text-field
                    class="mt-5"
                  v-model="amount"
                  type="number"
                  :counter="7"
                  :rules="amountRules"
                  label="Amount ($)"
                  required
                ></v-text-field>

                <v-select
                  v-model="select"
                  :items="loans"
                  :item-text="loans.text"
                  :item-value="loans.value"
                  :rules="[v => !!v || 'Item is required']"
                  label="Loan"
                  required
                ></v-select>

                <p  class="font-weight-bold">{{response}}</p>
                <v-btn
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
        </v-flex>
        
      </v-layout>
    </v-container>
    
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import axios from 'axios';

export default {
  name: "CreateLoanApp",
  components: {
  },
  created() {
      if(!localStorage.getItem('user-token')){
        this.$router.push('/login');
      }
      else if (localStorage.getItem('user-type') != 'CUST')
        this.$router.push('/');
      this.getLoans();
  },
  data: () => ({
      valid: true,
      amount: 0,
      amountRules: [
        v => !!v || 'This field is required',
        v => (v && v <= 1000000) || 'Must be less than 1000000',
      ],
      select: [],

      loans: [],
      response: '',
  }),

  methods: {
    getLoans() {
      axios.get('api/loans/', {
          headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
        })
        .then(resp => {
        //   console.log(resp.data);
            if (resp.data.length <= 0) {
                this.response = "Can not create a loan app, there is no loans available"
            }
          for (let i = 0; i < resp.data.length;  i++){
              this.loans.push({text:`${resp.data[i].id} - ${resp.data[i].loan_fund.fund_type}
               - ${resp.data[i].duration} years - ${resp.data[i].interest_rate}%`, value: resp.data[i].id})
          }
          console.log(this.loans);
        })
        .catch(err => {
          console.log(err);
        })  
    },

      validate () {
        if(this.$refs.form.validate()){
            console.log("loaaan", this.select)
          axios.post('api/loanapps/', {
                amount: this.amount,
                loan: this.select
            },
            {
                headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
          })
          .then(resp => {
            if (resp.data.error)
                this.response = resp.data.error;
            else
                this.response = 'Succefully created!'
          })
          .catch(err => {
            console.log(err);
            this.response = err;
          })  
        }
      },
  }
};
</script>

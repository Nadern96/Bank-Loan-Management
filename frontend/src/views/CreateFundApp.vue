<template>
  <div>
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md6>
          <v-card>
            <v-card-title>
              <h2 class="blue-grey--text">Invest in a Loan Fund</h2>
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
                  :counter="9"
                  :rules="amountRules"
                  label="Amount ($)"
                  required
                ></v-text-field>

                <v-select
                  v-model="select"
                  :items="loanfunds"
                  :item-text="loanfunds.text"
                  :item-value="loanfunds.value"
                  :rules="[v => !!v || 'Item is required']"
                  label="Loan Fund"
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
  name: "CreateFundApp",
  components: {
  },
  created() {
      if(!localStorage.getItem('user-token')){
        this.$router.push('/login');
      }
      else if (localStorage.getItem('user-type') != 'PROV')
        this.$router.push('/');
      this.getLoanFunds();
  },
  data: () => ({
      valid: true,
      amount: 0,
      amountRules: [
        v => !!v || 'This field is required',
        v => (v && v <= 100000000) || 'Must be less than 100000000',
      ],
      select: [],

      loanfunds: [],
      response: '',
  }),

  methods: {
    getLoanFunds() {
      axios.get('api/loanfunds/', {
          headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
        })
        .then(resp => {
        //   console.log(resp.data);
            if (resp.data.length <= 0) {
                this.response = "Can not create a loan, there is no loan funds available"
            }
          for (let i = 0; i < resp.data.length;  i++){
              this.loanfunds.push({text:`${resp.data[i].id} - ${resp.data[i].fund_type}
               - ${resp.data[i].duration} years - ${resp.data[i].interest_rate}%`, value: resp.data[i].id})
          }
        })
        .catch(err => {
          console.log(err);
        })  
    },

      validate () {
        if(this.$refs.form.validate()){
          axios.post('api/loanfundapps/', {
                amount: this.amount,
                loan_fund: this.select
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

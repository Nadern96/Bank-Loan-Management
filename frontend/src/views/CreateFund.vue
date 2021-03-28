<template>
  <div>
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md6>
          <v-card>
            <v-card-title>
              <h2 class="blue-grey--text">Create Loan Fund</h2>
            </v-card-title>
            <v-card-text>
              <v-form
                ref="form"
                v-model="valid"
                lazy-validation
              >
                <v-text-field
                  v-model="minamount"
                  type="number"
                  :counter="7"
                  :rules="minRules"
                  label="Min Amount ($)"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="maxamount"
                  type="number"
                  :counter="7"
                  :rules="maxRules"
                  label="Max Amount ($)"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="currentamount"
                  type="number"
                  :counter="10"
                  :rules="CurRules"
                  label="Initial Amount ($)"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="duration"
                  type="number"
                  min="1"
                  max="20"
                  :counter="2"
                  :rules="durationRules"
                  label="Duration (Yrs)"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="interest"
                  type="number"
                  :counter="2"
                  :rules="interestRules"
                  label="Interest Rate (%)"
                  required
                ></v-text-field>

               <v-select
                  v-model="fundtype"
                  :items="types"
                  :rules="[v => !!v || 'Item is required']"
                  label="Loan Fund Type"
                  required
                ></v-select>

                <p style="font-size:20px" class="font-weight-bold success--text">{{response}}</p>
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
import axios from 'axios';

export default {
  name: "CreateFund",
  components: {
  },
  created() {
      if(!localStorage.getItem('user-token')){
        this.$router.push('/login');
      }
      else if (localStorage.getItem('user-type') != 'Bank Per')
        this.$router.push('/');
  },
  data: () => ({
      valid: true,
      minamount: 0,
      maxamount: 0,
      currentamount: 1000000,
      minRules: [
        v => !!v || 'This field is required',
        v => (v && v >= 1000000 && v <= 10000000) || 'Must be  greater than or equal 1000000 and less than or equal to 10000000',
      ],
      maxRules: [
        v => !!v || 'This field is required',
        v => (v && v >= 10000000 && v <= 100000000) || 'Must be  greater than or equal 10000000 and less than or equal to 100000000',
      ],
      CurRules: [
        v => !!v || 'This field is required',
        v => (v && v>= 1000000 && v <= 100000000) || 'Must be greater than or equal 1000000 and less than or equal to 100000000',
      ],
      duration: 1,
    durationRules: [
        v => !!v || 'This field is required',
        v => (v && v <= 20) || 'Must be less than 20',
      ],
      interest: 1,
      interestRules: [
        v => !!v || 'This field is required',
        v => (v &&  v <= 30) || 'Must be less than 30',
      ],
      select: [],

      fundtype: null,
      types: [
        'Car',
        'Mortgage',
        'Personal',
      ],
      response: '',
  }),

  methods: {

      validate () {
        if(this.$refs.form.validate()){
            
                 axios.post('api/loanfunds/', {
                        min_amount: this.minamount,
                        max_amount: this.maxamount,
                        current_amount: this.currentamount,
                        duration: this.duration,
                        interest_rate: this.interest,
                        fund_type: this.fundtype
                    },
                    {
                        headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
                })
                .then(resp => {
                    console.log(resp.data);
                    this.response = 'Succefully created!'
                })
                .catch(err => {
                    console.log(err.data);
                    
                    this.response = err;
                })  
            
         
        }
      },
  }
};
</script>

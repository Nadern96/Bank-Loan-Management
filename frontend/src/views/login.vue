<template>
  <div class="login">
    
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md6>
          <v-card>
            <v-card-title>
              <h2 class="primary--text">Login</h2>
            </v-card-title>
            <v-card-text>
              <v-form
                ref="form"
                v-model="valid"
                lazy-validation
              >
                <v-text-field class="mt-6"
                  v-model="username"
                  :counter="20"
                  :rules="nameRules"
                  label="Username"
                  required
                ></v-text-field>

                <v-text-field class="mt-6"
                    v-model="password"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, rules.min]"
                    :type="show1 ? 'text' : 'password'"
                    name="input-10-1"
                    label="Password"
                    hint="At least 8 characters"
                    counter
                    @click:append="show1 = !show1"
                  ></v-text-field>

                <p class="font-weight-bold red--text">{{response}}</p>

                <v-btn
                  :disabled="!valid"
                  color="primary"
                  class="mr-4 mt-6"
                  @click="validate"
                >
                  Login  
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
  name: "login", 
  components: {
  },
  data: () => ({
      valid: true,
      username: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 20) || 'Name must be less than 20 characters',
      ],
      show1: false,
      password: 'Password',
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
      },
      response: '',
  }),

  methods: {
      validate () {
        if(this.$refs.form.validate()){
          axios.post('api/login/', {
            username: this.username,
            password: this.password,
          })
          .then(resp => {
            let token = resp.data.token,
                userType = resp.data.user_type,
                username = resp.data.username;
            localStorage.setItem('user-token', token);
            localStorage.setItem('user-type', userType);
            localStorage.setItem('username', username);

            // after succefful login go to home
            this.$router.push('/');
          })
          .catch(err => {
            console.log(err);
            localStorage.removeItem('user-token');
            this.response = 'Invalid Credentials'
          })  
        }
      },

  }
};
</script>

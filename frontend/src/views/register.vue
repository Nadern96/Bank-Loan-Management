<template>
  <div class="register">
    <v-container >
      <v-layout row mt-10 justify-center>
        <v-flex xs12 md6>
          <v-card>
            <v-card-title>
              <h2 class="primary--text">Register</h2>
            </v-card-title>
            <v-card-text>
              <v-form
                ref="form"
                v-model="valid"
                lazy-validation
              >
                <v-text-field
                  v-model="username"
                  :counter="20"
                  :rules="nameRules"
                  label="Username"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="email"
                  :rules="emailRules"
                  label="E-mail"
                  required
                ></v-text-field>

                <v-text-field
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

                <v-select
                  v-model="usertype"
                  :items="types"
                  :rules="[v => !!v || 'Item is required']"
                  label="User type"
                  required
                ></v-select>
                
                <v-btn
                  :disabled="!valid"
                  color="primary"
                  class="mr-4"
                  mt-5  
                  @click="validate"
                >
                  Register  
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
  name: "register", 
  components: {
  },
  data: () => ({
      valid: true,
      username: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 20) || 'Name must be less than 20 characters',
      ],
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      usertype: null,
      types: [
        'Bank Per',
        'PROV',
        'CUST',
      ],
      show1: false,
      password: 'Password',
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
      },
  }),

  methods: {
      validate () {
        if(this.$refs.form.validate()){
          axios.post('api/register/', {
            username: this.username,
            email: this.email,
            password: this.password,
            user_type: this.usertype
          })
          .then(resp => {
            let token = resp.data.token,
                userType = resp.data.user_type,
                username = resp.data.username;
            localStorage.setItem('user-token', token);
            localStorage.setItem('user-type', userType);
            localStorage.setItem('username', username);
            this.$router.push('/');
          })
          .catch(err => {
            console.log(err);
            localStorage.removeItem('user-token');
          })  
        }
      },
  }
};
</script>

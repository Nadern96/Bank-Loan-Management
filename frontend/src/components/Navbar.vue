<template>
    <nav class="mb-16">
            <v-app-bar fixed dense>
                <v-app-bar-nav-icon class="grey--text" @click="drawer=!drawer"></v-app-bar-nav-icon>
                <v-toolbar-title class="text-uppercase grey--text">
                    <span class="font-weight-light">Bank</span>
                    <span class="primary--text">Loan</span>
                </v-toolbar-title>


                
                <v-spacer></v-spacer>
                <v-btn plain color="primary text--lighten" @click="logout">    
                    <span>{{this.navLink}}</span>
                    <v-icon right>exit_to_app</v-icon>
                </v-btn>
                   
            </v-app-bar>
      
             <v-navigation-drawer   absolute temporary class="primary" v-model="drawer">
                <v-list  class="px-0 align-center justify-center fill-height">
                    <v-list-item v-for="link in links" :key="link.text" router :to="link.route">
                        <v-list-item-action>
                            <v-icon class="white--text">{{link.icon}}</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title class="white--text">
                                {{link.text}}
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-navigation-drawer>
            
        
    </nav>
</template>

<script>
export default {
  name: "Navbar",
  components: {
      
  },  
  created() {
      this.buildNavLinks();
      if(localStorage.getItem('user-token'))
        this.navLink = 'logout';
      else 
        this.navLink = 'register'   
    },
  data() {
      return {
          drawer: false,
          links: [
                {id: 0 ,icon: 'home', text: 'Home', route: '/' },
                // { icon: 'person', text: 'Team', route: '/team' },
            ],
            // navLink is one of these [login, register, logout]
            navLink: '',
      }
  },
  methods: {
      logout() {
        if(localStorage.getItem('user-token'))
        {
            localStorage.removeItem('user-token');   
            localStorage.removeItem('user-type');   
            localStorage.removeItem('username');   
            this.$router.push('/register');
        }
        else if (this.navLink == 'login') {
            this.$router.push('/login');
        }
        else {
            this.$router.push('/register');
        }
      },
      buildNavLinks() {
        if(localStorage.getItem('user-token'))
        {
            if(localStorage.getItem('user-type') === "Bank Per"){
                // to check that i haven't already build the nav
                for (let i=0; i<this.links.length; i++){
                    if(this.links[i].id === 1)
                        return;
                }
                if(this.links.length > 2)
                    this.links.splice(1);
                else 
                    this.links.splice(1,1);
                this.links.push({id:1, icon: 'money', text: 'Create Loan', route: '/createloan' });
                this.links.push({id:2, icon: 'money', text: 'Create Fund', route: '/createfund' });
                this.links.push({id:3, icon: 'folder', text: 'Fund Apps', route: '/fundapps' });
                this.links.push({id:4, icon: 'folder', text: 'Loan Apps', route: '/loanapps' });
            }
            else if(localStorage.getItem('user-type') === "CUST"){
                for (let i=0; i<this.links.length; i++){
                    if(this.links[i].id === 5)
                        return;
                    console.log("id   ", this.links[i].id)

                }
                if(this.links.length > 2)
                    this.links.splice(1);
                else 
                    this.links.splice(1);

                this.links.push({id:5, icon: 'money', text: 'Create Loan App', route: '/createloanapp' });
                this.links.push({id:6, icon: 'folder', text: 'My Apps', route: '/loanapps' });
            }
            else if(localStorage.getItem('user-type') === "PROV"){
                for (let i=0; i<this.links.length; i++){
                    if(this.links[i].id === 7)
                        return;
                    console.log("id   ", this.links[i].id)
                }
                if(this.links.length > 2)
                    this.links.splice(1);
                else 
                    this.links.splice(1,1);
                    
                this.links.push({id:7, icon: 'money', text: 'Create Fund App', route: '/createfundapp' });
                this.links.push({id:8, icon: 'folder', text: 'My Apps', route: '/fundapps' });
            }
        }
         else {
            if(this.links.length > 2)
                this.links.splice(1);
            else 
                this.links.splice(1,1);
        }
      }
  },
  watch:{
        $route (to, from){
            console.log(from);
            this.buildNavLinks();
            if(localStorage.getItem('user-token'))
            {
                this.navLink = 'logout';
            }
            else if(to.name === "login"){
                this.navLink = 'register'
            }
            else if(to.name === "register") {
                this.navLink = 'login'
            }
            else {
                this.navLink = 'register'   
            }
        }
    } 
};
</script>
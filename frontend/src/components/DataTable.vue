<template>
    <div class="data-table">
        <v-data-table
        :headers="headers"
        :items="data"
        item-key="name"
        class="elevation-1 mt-5 mb-5"
        @click:row="editRow"
        :search="search"
        >

        <template v-slot:top>
            <v-text-field
            v-model="search"
            label="Search"
            class="mx-4"
            ></v-text-field>
        </template>

        <template v-slot:item.delete="{ item }">
            <v-btn
            v-model="item.delete" 
            class="red white--text"
            @click="delItem(item)"
            :disabled = "item.status == 'Accepted'"
            >
                <v-icon>
                    delete
                </v-icon>
            </v-btn>
        </template>

        </v-data-table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "DataTable",
  components: {
  },  
  props: ['data', 'headers', 'goToLink'],
  created() {
        console.log('DataTable');  
        this.createPDF();
    },
  data() {
      return {
          search: '',
      }
  },
  methods: {
    delItem(item) {
        let id = item.id;
        let idx = this.data.indexOf(item);
        this.data.splice(idx, 1);
        
        axios.delete(`api${this.goToLink}${id}/`,
        {
            headers: {"Authorization" : `Token ${localStorage.getItem('user-token')}`},
        })
        .then(resp => {
            console.log(resp.data);
        })
        .catch(err => {
            console.log(err); 
        })  
    },
    editRow(row) {
        let route = this.$route.name;
        if (route === "ListFundApps"){
            this.$router.push(`/fundapps/${row.id}`);
        }
        else if (route === "ListLoanApps"){
            this.$router.push(`/loanapps/${row.id}`);
        }
    },
    createPDF () {
        console.log(this.data);
    }
  }
};
</script>
<template>
  <div class="searchBoxCollapsed">
    <b-container id="input-fields">
      <b-row>
        <b-col>
          <div class="inner">
            <img src="../assets/joogle_law_logo.png" width="100%">
          </div>
        </b-col>
        <b-col>
          <b-form-group label="Vorschrift">
            <b-form-input
              id="input-norm"
              v-model="search.norm"
              :data="search.suggestedNorms"
            ></b-form-input>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Suchbegriff">
            <b-form-input
              id="input-suchbegriff"
              v-model="search.suchbegriff"
              v-on:keyup.enter="loadResults"
            ></b-form-input>
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>

    <div id="results">
      <b-list-group>
        <b-list-group-item class="resultItems" v-bind:key="r.key" v-for="r in results">
          <ListItem v-bind:r="r" v-bind:search="search"></ListItem>
        </b-list-group-item>
      </b-list-group>
    </div>
  </div>
</template>

<script>
import API from "@/api/backend";
import _ from "underscore";

export default {
  name: "SearchResults",
  data() {
    return {
      search: {
        norm: "",
        suggestedNorms: [],
        suchbegriff: ""
      },
      results: []
    };
  },
  methods: {
    loadResults() {
      API.getResults(
        this.$data.search.suchbegriff,
        this.$data.search.norm,
        0,
        40
      ).then(data => {
        this.$data.results = data;
      });
    },
    getNormSuggestion() {
      API.getNormSuggestion(this.$data.search.norm).then(data => {
        this.$data.search.suggestedNorms = data;
      });
    }
  },
  created() {
    this.$data.search.norm = this.$route.params.norm;
    this.$data.search.suchbegriff = this.$route.params.searchTerm;
    this.loadResults();
  },
  computed: {
    searchTermComputed: function() {
      return this.$data.search.suchbegriff;
    },
    normComputed: function() {
      return this.$data.search.norm;
    },
    normInput: function () {
      return this.$data.search.norm;
    }
  },
  watch: {
    normInput: _.debounce(function(normInput) {
      this.getNormSuggestion();
    }, 200),
    searchTermComputed: function() {
      this.$router.replace({
        name: 'SearchResult',
        params: {
          norm: this.$data.search.norm,
          searchTerm: this.$data.search.suchbegriff
        }
      });
    },
    normComputed: function() {
      this.$router.replace({
        name: 'SearchResult',
        params: {
          norm: this.$data.search.norm,
          searchTerm: this.$data.search.suchbegriff
        }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.searchBoxCollapsed {
  width: 55%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  margin: auto;
}
img {
  max-width: 100%;
  max-height: 100%;
  display: block;
  margin: auto auto;
}
.inner {
  display: table-cell;
  height: 100px;
  width: 100%;
  vertical-align: middle;
}
</style>

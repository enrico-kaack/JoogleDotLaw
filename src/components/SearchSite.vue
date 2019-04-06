<template>
  <div>
    <div class="searchBoxCollapsed" v-if="showResults">
      <b-container id="input-fields">
        <b-row>
          <b-col>
            <div class="inner">
              <img src="../assets/joogle_law_logo.png" width="100%">
            </div>
          </b-col>
          <b-col>
            <b-form-group label="Vorschrift">
              <b-form-input id="input-norm" v-model="normInput"></b-form-input>
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

      <div id="results" v-if="showResults">
         <b-list-group>
      <b-list-group-item
        class="resultItems"
        v-bind:key="r.key"
        v-for="r in results"
      >
      <ListItem v-bind:r="r" v-bind:search="search"></ListItem>
      </b-list-group-item>
    </b-list-group>
      </div>
    </div>

    <div class="searchSite" v-bind:class="{gone: showResults}">
      <div class="searchBox">
        <b-container id="input-fields">
          <img src="../assets/joogle_law_logo.png" width="100%">
          <b-row>
            <b-col>
              <b-form-group label="Vorschrift">
                <vue-bootstrap-typeahead
                  id="input-norm"
                  v-model="normInput"
                  v-on:keyup.enter="loadNormText"
                  :data="search.suggestedNorms"
                  @hit="loadNormText"
                ></vue-bootstrap-typeahead>
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
          <b-row>
            <b-col>
              <b-form-group label="Normtext" v-on:keyup.enter="loadResults">
                <b-form-textarea
                  id="input-normtexxt"
                  v-model="search.normText"
                  @select.native="selectedText"
                  disabled
                  rows="3"
                ></b-form-textarea>
              </b-form-group>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
  </div>
</template>

<script>
import API from "@/api/backend";
import _ from "underscore";

export default {
  name: "SearchSite",
  data() {
    return {
      showResults: false,
      normInput: "",
      search: {
        suggestedNorms: [],
        suchbegriff: ""
      },
      results: [
        {
          key: "1",
          text:
            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
        }
      ]
    };
  },
  methods: {
    selectedText(event) {
      var indexStart = event.target.selectionStart;
      var indexEnd = event.target.selectionEnd;
      this.$data.search.suchbegriff = event.target.value.substring(
        indexStart,
        indexEnd
      );
    },
    loadNormText() {
      API.getNormText(this.$data.normInput).then(data => {
        var text = "";
        data.norm.text.forEach(t => {
          text += t + "\n";
        });
        this.$data.search.normText = text;
      });
    },
    getNormSuggestion() {
      API.getNormSuggestion(this.$data.normInput).then(data => {
        this.$data.search.suggestedNorms = data;
      });
    },

    loadResults() {
      this.$data.showResults = true;
      API.getResults(
        this.$data.search.suchbegriff,
        this.$data.normInput,
        0,
        10
      ).then(data => {
        this.$data.results = data;
      });
    },

    getLastFewWords(r, abs) {
      if (abs < 1 || r.urteil.absaetze[abs] === undefined) {
        return "";
      } else {
        var worte = r.urteil.absaetze[abs].text.split(" ");
        if (worte.length > 4) { worte = worte.slice(worte.length -4, worte.length)}
        return worte.join(" ");
      }
    },
    getFirstFewWords(r, abs) {
      return "";
    }
  },
  watch: {
    normInput: _.debounce(function(normInput) {
      this.getNormSuggestion();
    }, 200)
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


.searchSite {
  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 55%;
  height: 400px;
}

.goingTop {
  margin: 0 auto;
}

#results {
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
.gone {
  display: none;
}
</style>

<template>
  <div>


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
                  rows="8"
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
      this.$router.push({
        name: 'SearchResult',
        params: {
          norm: this.$data.normInput,
          searchTerm: this.$data.search.suchbegriff
        }
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



.searchSite {
  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 55%;
  height: 600px;
}

.goingTop {
  margin: 0 auto;
}

#results {
}


.gone {
  display: none;
}
</style>

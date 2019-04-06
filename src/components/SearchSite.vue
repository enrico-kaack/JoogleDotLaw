<template>
  <div>
    <div class="searchBoxCollapsed" v-if="showResults">
      <b-container id="input-fields">
        <b-row>
          <b-col>
            <img src="../assets/joogle_law_logo.png" width="100%">
          </b-col>
          <b-col>
            <b-form-group label="Vorschrift">
              <b-form-input id="input-norm" v-model="norm"></b-form-input>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Suchbegriff">
              <b-form-input id="input-suchbegriff" v-model="suchbegriff"></b-form-input>
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
          >{{ r.text }}</b-list-group-item>
        </b-list-group>
      </div>
    </div>

    <div class="searchSite" v-bind:class="{goingTop: showResults}">
      <div class="searchBox" v-if="!showResults">
        <b-container id="input-fields">
          <img src="../assets/joogle_law_logo.png" width="100%">
          <b-row>
            <b-col>
              <b-form-group label="Vorschrift">
                <b-form-input id="input-norm" v-model="norm" v-on:click="loadNormText"></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="Suchbegriff">
                <b-form-input id="input-suchbegriff" v-model="suchbegriff"></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group label="Normtext">
                <b-form-textarea id="input-normtexxt" v-model="normText" rows="3"></b-form-textarea>
              </b-form-group>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchSite",
  data() {
    return {
      showResults: false,
      search: {
        norm: "",
        normText: "",
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
    loadNormText: () => {
      
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

.resultItems {
  position: relative;
}

.resultItems::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background: -webkit-linear-gradient(
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 1) 100%
  );
  background-image: -moz-linear-gradient(
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 1) 100%
  );
  background-image: -o-linear-gradient(
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 1) 100%
  );
  background-image: linear-gradient(
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 1) 100%
  );
  background-image: -ms-linear-gradient(
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 1) 100%
  );
}

.resultItems::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background: -webkit-linear-gradient(
    rgba(255, 255, 255, 1) 0%,
    rgba(255, 255, 255, 0) 100%
  );
  background-image: -moz-linear-gradient(
    rgba(255, 255, 255, 1) 0%,
    rgba(255, 255, 255, 0) 100%
  );
  background-image: -o-linear-gradient(
    rgba(255, 255, 255, 1) 0%,
    rgba(255, 255, 255, 0) 100%
  );
  background-image: linear-gradient(
    rgba(255, 255, 255, 1) 0%,
    rgba(255, 255, 255, 0) 100%
  );
  background-image: -ms-linear-gradient(
    rgba(255, 255, 255, 1) 100%,
    rgba(255, 255, 255, 0) 0%
  );
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
</style>

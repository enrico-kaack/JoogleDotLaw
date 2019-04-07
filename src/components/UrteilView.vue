<template>
  <div>
    <b-container>
      <b-row>
        <b-col>{{r.urteil.gertyp}}</b-col>
        <b-col>{{r.urteil.doktyp}}</b-col>
        <b-col>{{r.urteil.aktenzeichen}}</b-col>
        <b-col>{{dateFormatted}}</b-col>
      </b-row>
      <b-row>
        <b-col>
          <h5>{{r.urteil.titel.replace(/<(?:.|\n)*?>/gm, '')}}</h5>
        </b-col>
      </b-row>
      <b-row>
        <div>
          <b-card title="Tenor" tag="article">
            <b-card-body>
              <div v-html="r.urteil.tenor"></div>
            </b-card-body>
          </b-card>
        </div>
      </b-row>
      <b-row>
        <div>
          <b-card title="Gründe" tag="article">
            <b-card-body>
              <div v-html="textFormatted"></div>
            </b-card-body>
          </b-card>
        </div>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "UrteilView",
  props: ["r", "search"],
  created() {
    console.log("updated");
    setTimeout(() => {
      var elToScrollTo = document.getElementsByName("rd_" + this.$props.r.abs);
      console.log(elToScrollTo);
      this.$scrollTo(elToScrollTo[0], { offset: -60 });
    }, 500);
  },
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
  },
  computed: {
    dateFormatted: function() {
      var date = moment(this.$props.r.urteil.entschDatum);
      return date.format("DD.MM.YYYY");
    },
    textFormatted: function() {
      var text = this.$props.r.urteil.gruende;
      text = text.replace(
        new RegExp(this.$props.search.suchbegriff, "g"),
        "<spawn class='marked' style='background-color: rgb(249, 253, 10);'>" +
          this.$props.search.suchbegriff +
          "</spawn>"
      );
      return text;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

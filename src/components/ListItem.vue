<template>
  <div>
      <b-button
        id="refButton"
        v-on:click="navToUrteil"
        variant="light"
      >{{r.urteil.gertyp}} {{r.urteil.doktyp}} vom {{dateFormatted}} - Az. {{r.urteil.aktenzeichen}}</b-button>
    <div class="resultItem beforeItem afterItem">
      {{ textBefore }}
      <br v-if="textBefore !== ''">
      <br>
      <div v-html="textFormatted"></div>
      <br v-if="textBefore !== ''">
      <br>
      {{ textAfter }}
    </div>
    <div class="feedback">
      <b-button variant="outline-secondary" v-bind:pressed="pressed == 1" v-on:click="pressed = 1">Sehr schlecht</b-button>
      <b-button variant="outline-secondary" v-bind:pressed="pressed == 2" v-on:click="pressed = 2">Schlecht</b-button>
      <b-button variant="outline-secondary" v-bind:pressed="pressed == 3" v-on:click="pressed = 3">Gut</b-button>
      <b-button variant="outline-secondary" v-bind:pressed="pressed == 4" v-on:click="pressed = 4">Sehr gut</b-button>
      </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "ListItem",
  props: ["r", "search"],
  data() {
    return {
      pressed: 0,
      feedbackLabels: ["Schlecht", "Mittel", "Gut"]
    };
  },
  computed: {
    abs: function() {
      return this.$props.r.abs - 1; //absatz notation starts at 1
    },

    dateFormatted: function() {
      var date = moment(this.$props.r.urteil.entschDatum);
      return date.format("DD.MM.YYYY");
    },

    textBefore: function() {
      var abs = this.abs - 1;
      if (abs < 1 || this.$props.r.urteil.absaetze[abs] === undefined) {
        return "\n";
      } else {
        var worte = this.$props.r.urteil.absaetze[abs].text.split(" ");
        if (worte.length > 4) {
          worte = worte.slice(worte.length - 4, worte.length);
        }
        return worte.join(" ");
      }
    },

    textFormatted: function() {
      var text = this.$props.r.urteil.absaetze[this.$props.r.abs - 1].text;
      text = text.replace(
        new RegExp(this.$props.search.suchbegriff, "g"),
        "<spawn class='marked' style='background-color: rgb(249, 253, 10);'>" +
          this.$props.search.suchbegriff +
          "</spawn>"
      );
      return text;
    },

    textAfter: function() {
      var abs = this.abs + 1;
      if (
        abs > this.$props.r.urteil.absaetze.length ||
        this.$props.r.urteil.absaetze[abs] === undefined
      ) {
        return "";
      } else {
        var worte = this.$props.r.urteil.absaetze[abs].text.split(" ");
        if (worte.length > 4) {
          worte = worte.slice(0, 4);
        }
        return worte.join(" ") + "...";
      }
    }
  },
  methods: {
    navToUrteil() {
      this.$router.push({
        name: "Urteil",
        params: {
          az: this.$props.r.urteil.aktenzeichen,
          r: this.$props.r,
          search: this.$props.search
        }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.resultItems {
  position: relative;
}

.afterItem::after {
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

.beforeItem::before {
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
.feedback {
  position: absolute;
  bottom: 0;
  right: 0;
  z-index: 1;
  margin: 5px;
}

#refButton {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 1;
  margin: 5px;
}
</style>

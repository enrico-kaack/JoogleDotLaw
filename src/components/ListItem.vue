<template>
  <div>
    <div class="resultItem beforeItem afterItem">
      {{ textBefore }}
      <br v-if="textBefore !== ''">
      <br>
      {{ r.urteil.absaetze[abs].text }}
      <br v-if="textBefore !== ''">
      <br>
      {{ textAfter }}
    </div>
  </div>
</template>

<script>
export default {
  name: "ListItem",
  props: ["r"],
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
  },
  computed: {
    abs: function() {
      return this.$props.r.abs - 1; //absatz notation starts at 1
    },

    textBefore: function() {
      var abs = this.abs - 1;
      console.log(abs);
      if (abs < 1 || this.$props.r.urteil.absaetze[abs] === undefined) {
        return "";
      } else {
        console.log(
          "absätze",
          this.$props.r.urteil.absaetze[abs],
          this.$props.r.urteil.absaetze[abs].text
        );
        var worte = this.$props.r.urteil.absaetze[abs].text.split(" ");
        if (worte.length > 4) {
          worte = worte.slice(worte.length - 4, worte.length);
        }
        console.log(worte);
        return worte.join(" ");
      }
    },

    textAfter: function() {
      var abs = this.abs + 1;
      if (
        abs > this.$props.r.urteil.absaetze.length ||
        this.$props.r.urteil.absaetze[abs] === undefined
      ) {
        return "";
      } else {
        console.log(
          "absätze",
          this.$props.r.urteil.absaetze[abs],
          this.$props.r.urteil.absaetze[abs].text
        );
        var worte = this.$props.r.urteil.absaetze[abs].text.split(" ");
        if (worte.length > 4) {
          worte = worte.slice(0, 4);
        }
        console.log(worte);
        return worte.join(" ") + "...";
      }
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
</style>

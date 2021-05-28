<template lang="pug">
#range
  div(v-if="value.length != 0")
    v-range-slider.py-12.my-12(
      thumb-label="always",
      color="blue",
      v-model="val",
      step="10",
      style="width: 100%",
      :min="getMin()",
      :max="getMax()"
    )
    v-btn(
      block,
      color="blue",
      dark,
      rounded,
      :disabled="value.length == 0",
      @click="selectOption()"
    ) Siguiente
  div(v-else)
    v-alert(type="error") No hemos encontrado monitores con estas características
    v-btn(block, color="blue", dark, rounded, @click="repeat()") Repetir Test
</template>

<script>
export default {
  props: ["question", "value"],
  created() {
    this.left = this.getMin();
    this.right = this.getMax();
    this.val = [this.getMin(), this.getMax()];
  },
  methods: {
    repeat() {
      location.reload();
    },
    getMin() {
      let min = 9007199254740991;

      this.value.forEach((el) => {
        min = el.node.price < min ? el.node.price : min;
        console.log(min);
      });

      return min;
    },
    getMax() {
      let max = -9007199254740991;

      this.value.forEach((el) => {
        max = el.node.price > max ? el.node.price : max;
      });

      console.log(max);

      return max;
    },
    selectOption() {
      if (this.val[0] > this.val[1]) {
        this.val[1] = [this.val[0], (this.val[0] = this.val[1])][0]; //SWAP
      }

      this.$emit(
        "input",
        this.value.filter(
          (el) => el.node.price >= this.val[0] && el.node.price <= this.val[1]
        )
      );

      this.$emit("next", this.question.next);
    },
  },
};
</script>
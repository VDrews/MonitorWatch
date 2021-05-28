<template lang="pug">
#test
  div(v-if="!isResult")
    v-layout(align-center)
      .ml-3.font-weight-light(style="font-size: 2em") {{ questions[actualTest].question }}
    .ml-4.subtitle {{ questions[actualTest].description }}
    component(
      :is="questions[actualTest].type",
      :question="questions[actualTest]",
      v-model="monitores",
      @next="nextTest",
      transition="fade",
      transition-mode="out-in"
    ) 
  div(v-else)
    .font-weight-light(style="font-size: 2em") Te recomendamos estos Monitores
    .subtitle Según los gustos que nos has indicado
    v-btn.mt-4.text-capitalize(text, @click="resetTest") Repetir Test
    v-layout.mt-4(wrap)
      v-flex.pa-1(xs6, md3, v-for="(el, i) in monitores", :key="i")
        product(:product="el", style="height: 100%")
</template>

<static-query>
query {
  allProductPost {
    totalCount,
    edges {
      node {
        name,
        image,
        brand,
        price,
        inches,
        res,
        url,
        tags,
        show,
        res_time,
        frec
      }
    }
  }
}
</static-query>

<script>
import questionsData from "../test/monitores.json";
import question from "@/components/question.vue";
import range from "@/components/range.vue";
import images from "@/components/images.vue";
import product from "@/components/product.vue";

export default {
  components: {
    question,
    range,
    images,
    product,
  },
  data() {
    return {
      isResult: false,
      actualTest: 0,
      questions: questionsData,
      monitores: null,
    };
  },
  methods: {
    nextTest(val) {
      console.log("EMITTED", val);
      console.log(this.monitores);
      if (val == -1) {
        this.isResult = true;
      } else {
        this.actualTest = val;
      }
    },
    resetTest() {
      this.actualTest = 0;
      this.isResult = false;
      this.monitores = this.$page.allProductPost.edges;
    },
  },
  mounted() {
    this.monitores = this.$page.allProductPost.edges;
  },
};
</script>

<style>
.fade-transition {
  transition: opacity 1s ease;
}

.fade-enter,
.fade-leave {
  opacity: 0;
}
</style>
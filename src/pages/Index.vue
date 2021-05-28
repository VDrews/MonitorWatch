<template lang="pug">
Layout
  v-app
    v-layout.mt-12(column, align-center, style="width: 100vw")
      v-card.elevation-12(
        :class="{ 'mt-12': $vuetify.breakpoint.mdAndUp }",
        style="width: 100%; max-width: 1000px"
      )
        .pa-6.pb-6(style="max-width: 1000px; width: 100%")
          h1 MonitorWatch
          p Encuentra Monitor de la manera más sencilla haciendo nuestro test
          test
        //- h2 🔥 Los {{page.product}} más comprados
        //- v-layout.mt-4(wrap)
        //-   v-flex.pa-1(xs6, md3, v-for="(el, i) in monitores", :key="i")
        //-     product(:product="el", style="height: 100%")
        //- h2 Otros Tests
</template>

<page-query>
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
</page-query>

<script>
import Test from "@/layouts/test.vue";
import Product from "@/components/product.vue";

export default {
  metaInfo: {
    title: "Encuentra tu monitor",
    description: "Encuentra tu monitor ideal",
  },
  components: {
    Test,
    Product,
  },
  data() {
    return {
      found: true,
      monitores: [],

      pageName:
        this.$router.history.current.path.charAt(1).toUpperCase() +
        this.$router.history.current.path.slice(2),
    };
  },
  methods: {
    toAmazon(link) {
      window.open(link);
    },
  },
  mounted() {
    this.monitores = this.$page.allProductPost.edges
      .map((node) => node.node)
      .sort(function (first, second) {
        return first.tags.includes("Choice") && second.tags.includes("Choice")
          ? 0
          : first.tags.includes("Choice")
          ? -1
          : 1;
      })
      .slice(0, 8);
  },
  // async asyncData({ $content, redirect, params }) {
  //   let page;
  //   try {
  //     page = await $content("monitores").fetch();
  //   } catch (err) {
  //     redirect(`/notFound`);
  //   }

  //   return {
  //     page
  //   };
  // }
};
</script>


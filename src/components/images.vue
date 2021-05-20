<template lang="pug">
  #question
    v-layout(wrap)
      v-flex.pa-2(xs6, md3, v-for="(option, i) in question.options", :key="i")
        v-card.pb-10(outlined, hover, @click="selectOption(option)", style="height: 100%")
          v-img(:src="option.image")
          .pa-4
            b.mt-3 {{ option.answer }}
            .subtitle {{ option.description }}
</template>

<script>
import select from "@/mixins/select";
export default {
  props: ["question", "value"],
  mixins: [select]
};
</script>
<template lang="pug">
  #question
    v-list
      v-list-item.mt-3(v-for="(option, i) in question.options", three-line, :key="i", @click="selectOption(option)", color="blue") 
        v-list-item-content
          v-list-item-title {{ option.answer }}
          v-list-item-subtitle {{ option.description }}
</template>

<script>
import select from "@/mixins/select";
export default {
  props: ["question", "value"],
  mixins: [select]
};
</script>
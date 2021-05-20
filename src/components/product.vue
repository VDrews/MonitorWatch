<template lang="pug">
  #product
    v-card.pb-12.my-2(outlined, hover, @click="toDynos(product.node.url)", style="height: 100%")
      .pa-4
        v-img(:src="product.node.image", style="height: 200px; object-fit: cover;")
        .font-weight-light.mt-3 {{ product.node.name | truncate }}
        v-layout(justify-space-between)
          .font-weight-bold {{ product.node.price }}€
          v-chip.font-weight-bold(v-if="product.node.tags.includes('Choice')", small, color="yellow darken-3") Recomendado
        v-layout(wrap)
          v-chip.font-weight-bold.mr-2.my-2(v-for="(chip, c) in product.node.show", :key="c", small) {{chip}}
      v-btn.text-capitalize(color="red", tile, @click.stop="openVideo(product.node.name)", block, depressed, small, style="position: absolute; bottom: 32px; left: 0; right: 0") 
        v-icon.mr-3(small) mdi-youtube
        span(style="letter-spacing: 0") Ver Review
      v-btn.text-capitalize(color="orange", tile, block, depressed, small, style="position: absolute; bottom: 0; left: 0; right: 0") 
        v-icon.mr-3(small) mdi-basket
        span(style="letter-spacing: 0") Comprar en Dynos
    v-dialog(:value="videoUrl")
      v-card
        v-layout(column, align-center)
          h2.ma-2 Review del Monitor
          iframe(v-if="videoUrl", :src="videoUrl", frameBorder="0", width="1000", height="600")
          v-btn.ma-2(fab, @click="videoUrl = null")
            v-icon mdi-close
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      videoUrl: null,
    }
  },
  filters: {
    truncate(value) {
      if (value.length > 40) {
        return value.substr(0, 40) + "..."
      } else {
        return value
      }
    }
  },
  props: ["product"],
  methods: {
    toDynos(link) {
      window.open(link);
    },
    async openVideo(name) {
      try {
        const {data} = await axios.get(`https://www.googleapis.com/youtube/v3/search?part=id&q=${name}&key=AIzaSyBwbwAWzgtBNgutcxq7663I9JDKXEGJEOA`)
        console.log(data)
        this.videoUrl = 'https://www.youtube.com/embed/' + data.items[0].id.videoId
        console.log(this.videoUrl)
      } catch(err) {
        console.error(err)
      }
    
    },
  }
};
</script>
<template lang="pug">
#product
  v-card.pb-12.my-2(
    outlined,
    hover,
    @click="toDynos(product.node.url)",
    style="height: 100%"
  )
    .pa-4
      v-img(
        :src="product.node.image",
        style="height: 200px; object-fit: cover"
      )
      .font-weight-light.mt-3 {{ product.node.name | truncate }}
      v-layout(justify-space-between)
        .font-weight-bold {{ product.node.price }}€
        v-chip.font-weight-bold(
          v-if="product.node.tags.includes('Choice')",
          small,
          color="yellow darken-3"
        ) Recomendado
      v-layout(wrap)
        v-tooltip(bottom, v-for="(chip, c) in product.node.show", :key="c")
          template(v-slot:activator="{ on, attrs }")
            v-chip.font-weight-bold.mr-2.my-2(
              small,
              @click.stop="openWiki",
              v-on="on",
              @mouseover="getWikiInfo(chip)"
            ) {{ chip }}
          span(v-if="!wikiInfo") Cargando Información
          div(v-else)
            span {{ wikiInfo }}
            .font-weight-bold Haz click para ver el artículo completo
    v-btn.text-capitalize(
      color="red",
      tile,
      @click.stop="openVideo(product.node.name)",
      block,
      depressed,
      small,
      style="position: absolute; bottom: 32px; left: 0; right: 0"
    ) 
      v-icon.mr-3(small) mdi-youtube
      span(style="letter-spacing: 0") Ver Review
    v-btn.text-capitalize(
      color="orange",
      tile,
      block,
      depressed,
      small,
      style="position: absolute; bottom: 0; left: 0; right: 0"
    ) 
      v-icon.mr-3(small) mdi-basket
      span(style="letter-spacing: 0") Comprar en Dynos
  v-dialog(:value="videoUrl")
    v-card
      v-layout(column, align-center)
        h2.ma-2 Review del Monitor
        iframe(
          v-if="videoUrl",
          :src="videoUrl",
          frameBorder="0",
          width="1000",
          height="600"
        )
        v-btn.ma-2(fab, @click="videoUrl = null")
          v-icon mdi-close
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      videoUrl: null,
      wikiInfo: null,
      wikiPage: null,
    };
  },
  filters: {
    truncate(value) {
      if (value.length > 40) {
        return value.substr(0, 40) + "...";
      } else {
        return value;
      }
    },
  },
  props: ["product"],
  methods: {
    toDynos(link) {
      window.open(link);
    },
    async openVideo(name) {
      try {
        const { data } = await axios.get(
          `https://www.googleapis.com/youtube/v3/search?part=id&q=${name}&key=AIzaSyBwbwAWzgtBNgutcxq7663I9JDKXEGJEOA`
        );
        console.log(data);
        this.videoUrl =
          "https://www.youtube.com/embed/" + data.items[0].id.videoId;
        console.log(this.videoUrl);
      } catch (err) {
        console.error(err);
      }
    },
    async getWikiInfo(name) {
      let searchterm = name;
      if (name == "Gaming") searchterm = "Videojuego";
      else if (name == "1ms") searchterm = "Frecuencia de Refresco";
      else if (name == "Alta Tasa Refresco")
        searchterm = "Frecuencia de Refresco";
      else if (name == "Gigante") searchterm = "Televisor";
      else if (name == "Curvo") searchterm = "Curvatura";
      else if (name == "IPS") searchterm = "TFT LCD";
      else if (name == "QHD") searchterm = "1440p";
      else if (name == "4K") searchterm = "Resolución 4K";
      else if (name == "Altura Regulable")
        searchterm = "Video Electronics Standards Association";
      else if (name == "Tipo C") searchterm = "USB-C";
      else if (name == "Ultrawide") searchterm = "Relación de aspecto";
      const { data } = await axios.get(
        `https://es.wikipedia.org/w/api.php?action=query&list=search&srprop=snippet&format=json&origin=*&utf8=&srsearch=${searchterm}`
      );

      this.wikiPage = `https://es.wikipedia.org/?curid=${data.query.search[0].pageid}`;
      this.wikiInfo = this.stripHtml(data.query.search[0].snippet);
    },
    openWiki() {
      window.open(this.wikiPage);
    },
    stripHtml(html) {
      let tmp = document.createElement("div");
      tmp.innerHTML = html;
      return tmp.textContent || tmp.innerText || "";
    },
  },
};
</script>

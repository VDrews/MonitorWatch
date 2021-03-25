<template>
  <Layout>

    <!-- Learn how to use images here: https://gridsome.org/docs/images -->
    <g-image alt="Example image" src="~/favicon.png" width="135" />

    <h1>Bienvenido a Monitor Watch!!</h1>

    <p>
      MonitorWatch es un recomendador de monitores donde con un sencillo test te encontramos los monitores más acordes a tus necesidades
    </p>

    <p class="home-links">
      <a href="https://github.com/VDrews/MonitorWatch" target="_blank" rel="noopener">GitHub</a>
    </p>

  </Layout>
</template>

<script>
export default {
  metaInfo: {
    title: 'Hello, world!'
  }
}
</script>

<style>
.home-links a {
  margin-right: 1rem;
}
</style>

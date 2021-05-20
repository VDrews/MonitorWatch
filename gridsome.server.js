// Server API makes it possible to hook into various parts of Gridsome
// on server-side and add custom data to the GraphQL data layer.
// Learn more: https://gridsome.org/docs/server-api/

// Changes here require a server restart.
// To restart press CTRL + C in terminal and run `gridsome develop`

const nodeExternals = require('webpack-node-externals')
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  name: String,
  brand: String,
  img: String,
  url: String,
  price: Number,
  inches: Number,
  res: Number,
  tags: [String],
  show: [String],
  res_time: Number,
  frec: Number,
});

module.exports = function (api) {
  api.chainWebpack((config, { isServer }) => {
    if (isServer) {
      config.externals([
        nodeExternals({
          allowlist: [/^vuetify/]
        })
      ])
    }
  })

  api.loadSource(async ({ addCollection }) => {
    const Product = mongoose.model('monitores', productSchema);
    await mongoose.connect('mongodb+srv://versy:u9kdNWiNt2bk6DwD@cluster0.xx7nr.mongodb.net/monitorwatch', {useNewUrlParser: true, useUnifiedTopology: true});
    const db = mongoose.connection

    console.log('MONGO FUNCIONA')
    
    const products = await Product.find({}).lean()
    console.log(products)
    const productCollection = addCollection({
      typeName: "productPost",
    });

    // Añadimos cada tweet en la Base de datos con addNode
    // productCollection.addNode({ 
    //   name: 'test',
    //   brand: 'Marca',
    //   price: 480,
    //   image: "https://cdn.grupoelcorteingles.es/SGFM/dctm/MEDIA03/201906/21/00115216115806____1__640x640.jpg",
    //   inches: 18,
    //   res: 2070,
    //   tags: ["Gaming", "Audio"],
    //   show: ["Gaming"],
    //   res_time: 15,
    //   frec: 144,
    //  });
    // productCollection.addNode({ 
    //   name: 'test',
    //   brand: 'Marca',
    //   price: 680,
    //   image: "https://cdn.grupoelcorteingles.es/SGFM/dctm/MEDIA03/201906/21/00115216115806____1__640x640.jpg",
    //   inches: 18,
    //   res: 2070,
    //   tags: ["Gaming", "Audio"],
    //   show: ["Gaming"],
    //   res_time: 15,
    //   frec: 144,
    //  });
    for (const product of products) {
      productCollection.addNode({
        name: product.name,
        brand: product.brand,
        price: product.price,
        image: product.img,
        inches: product.inches,
        res: product.res,
        tags: product.tags,
        url: product.url,
        show: product.show,
        res_time: product.res_time,
        frec: product.frec,
      });
    }

    db.close()
      // we're connected!
    // Use the Data Store API here: https://gridsome.org/docs/data-store-api/
  })

  api.createPages(({ createPage }) => {
    // Use the Pages API here: https://gridsome.org/docs/pages-api/
  })
}

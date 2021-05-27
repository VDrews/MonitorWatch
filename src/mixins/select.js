let mixin = {
  methods: {
    selectOption(option) {
      let products = [...this.value]
      console.log("BEFORE", products)
      if (typeof option.moreThan != 'undefined' && option.moreThan != {}) {
        for (let key in option.moreThan) {
          products = products.filter(el => el.node[key] >= option.moreThan[key])
          console.log("AFTER", products)
          this.$emit(
            "input",
            products
          );
        }
      }
      if (typeof option.contains != 'undefined' && option.contains != {}) {
        for (let key in option.contains) {
          products = products.filter(el => el.node.tags.includes(option.contains[key]))
          console.log("AFTER", products)
          this.$emit(
            "input",
            products
          );
        }

      }
      if (typeof option.equals != 'undefined' && option.equals != {}) {
        for (let key in option.equals) {
          products = products.filter(el => el.node[key] == option.equals[key])
          console.log("AFTER", products)
          this.$emit(
            "input",
            products
          );
        }

      }

      if (typeof option.notEquals != 'undefined' && option.notEquals != {}) {
        for (let key in option.equals) {
          products = products.filter(el => el.node[key] != option.notEquals[key])
          console.log("AFTER", products)
          this.$emit(
            "input",
            products
          );
        }

      }


      if (typeof option.lessThan != 'undefined' && option.lessThan != {}) {
        for (let key in option.lessThan) {
          products = products.filter(el => el.node[key] <= option.lessThan[key])
          console.log("AFTER", products)
          this.$emit(
            "input",
            products
          );
        }
      }

      if (typeof option.between != 'undefined' && option.between != {}) {
        for (let key in option.between) {
          products = products.filter(el => (el.node[key] >= option.between[key][0] && el.node[key] <= option.between[key][1]))
          console.log("AFTER", products)
          this.$emit(
            "input",
            products
          );
        }
      }

      if (typeof option.orderByTag != 'undefined') {
        products = products.sort(function (first, second) {
          // Contain values first
          return (first.node.tags.includes(option.orderByTag) && second.node.tags.includes(option.orderByTag)) ? 0 : first.node.tags.includes(option.orderByTag) ? -1 : 1;
        })
        console.log("AFTER", products)
        this.$emit(
          "input",
          products
        )
      }

      this.$emit("next", option.next);
    }
  }
}

export default mixin

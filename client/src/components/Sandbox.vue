<!-- Vue component -->
<template>
  <div>
    here in sandbox
  </div>
</template>
<script>
const urlSearchParams = new URLSearchParams(window.location.search);
console.log(urlSearchParams)
const params = Object.fromEntries(urlSearchParams.entries());
console.log("query params", params)
// console.log('query params:', this.$route.query)

// import Multiselect from 'vue-multiselect'
// import JwPagination from 'jw-vue-pagination';

export default {
  mounted() {
    console.log(this.$route.query) // outputs 'yay'
  }
}
</script>

<!-- New step!
     Add Multiselect CSS. Can be added as a static asset or inside a component. -->
<!--<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>-->

<style scoped>
.tab-content {
  display: none
}

.tab-link {
  transition: .2s ease-in-out;
}

.tab-link.active {
  @apply bg-gray-400 font-bold;
}

</style>

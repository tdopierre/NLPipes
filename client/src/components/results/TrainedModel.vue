<template>
  <div class="p-3">
    <div>
      <div class="text-xl font-bold mb-3">
        Model Metrics
      </div>
      <div class="p-3 bg-gray-100 rounded-md flex">
        <div class="w-auto">
          <div v-for="(value, key) in resultData.metrics" v-bind:key="key" class="flex items-center ">
            <div class="block uppercase tracking-wide text-gray-700 text-sm font-bold mr-4">{{ key }}</div>
          </div>
        </div>
        <div class="w-full">
          <div v-for="(value, key) in resultData.metrics" v-bind:key="key" class="flex items-center ">
            <div class="block uppercase tracking-wide text-gray-700 text-sm mr-4">{{ value }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
export default {
  data() {
    return {}
  },
  props: {
    resultData: {
      type: Object,
      metrics: {
        type: Object
      }
    }
  },
  mounted() {
  }
}
</script>
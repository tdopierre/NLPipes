<template>
    <div>
<!--        <p>-->
        <!--            KMeansForm-->
        <!--            model_config {{ JSON.stringify(model_config)}}-->
        <!--            model_config_ {{ JSON.stringify(model_config_)}}-->

        <!--        </p>-->

        <b-input-group prepend="#Clusters" class="mb-2" :append="model_config.n_clusters.toString()">
            <b-form-input
                    required
                    id="kMeansForm-nClusters"
                    type='range'
                    min="5"
                    max="100"
                    step="1"
                    @change="configChange"
                    v-model.number="model_config.n_clusters"></b-form-input>
        </b-input-group>
    </div>
</template>

<script>
export default {
  name: 'KMeansForm',
  props: {
    model_config: {
      type: Object,
      default() {
        return {
          n_clusters: 0,
        };
      },
    },
  },
  data() {
    return {
      model_config_: null,
    };
  },
  mounted() {
    this.model_config_ = this.model_config;
  },
  methods: {
    configChange() {
      this.$emit('model-config-change', this.model_config_);
    },
  },
};
</script>

<template>
    <div>
        <b-input-group prepend="Model" class="mb-2">
            <b-form-select
                    class=""
                    v-on:change="modelConfigChange({})"
                    :options="['kmeans']"
                    v-model="model_class_"
                    required>
            </b-form-select>
        </b-input-group>
<!--        <p>ClusteringForm model_config_ {{ JSON.stringify(this.model_config_)}}</p>-->
        <KMeansForm
                v-if="this.model_class_==='kmeans'"
                @model-config-change="modelConfigChange"
                :model_config="this.model_config_"
        />

    </div>
</template>

<script>
import KMeansForm from './kmeans/KMeansForm.vue';

export default {
  name: 'ClusteringForm',
  props: {
    id: Number,
    model_class: String,
    model_config: {
      n_clusters: null,
    },
  },
  data() {
    return {
      model_class_: null,
      model_config_: {
        n_clusters: null,
      },
    };
  },
  mounted() {
    this.model_class_ = this.model_class;
    this.model_config_ = this.model_config;
    console.log('ClusteringForm mounted!', this.model_class_, this.model_config_);
  },
  methods: {
    modelConfigChange(newConfig) {
      console.log('config is changing with event', newConfig);
      this.model_config_ = newConfig;
      this.$emit('model-change', {
        model_class: this.model_class_,
        model_config: this.model_config_,
      });
    },
  },
  components: {
    KMeansForm,
  },
};
</script>

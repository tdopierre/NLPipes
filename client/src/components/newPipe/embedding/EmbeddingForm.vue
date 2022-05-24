<template>
    <div>
        <b-input-group prepend="Embedder" class="my-2">
            <b-form-select
                    class="m-0"
                    v-model="embedder_class_"
                    :options="['random','tfidf','transformer']"
                    v-on:change="embedderChange"
                    required>

            </b-form-select>
        </b-input-group>

        <TransformerEmbedderForm class=""
                                 v-if="embedder_class_==='transformer'"
                                 :embedder_config="embedder_config_"
                                 @embedder-config-change="embedderConfigChange"
        />
        <TfIdfForm class=""
                   v-if="embedder_class_==='tfidf'"
                   @embedder-config-change="embedderConfigChange"
        />
    </div>
</template>

<script>
import TransformerEmbedderForm from './transformer/TransformerEmbedderForm.vue';
import TfIdfForm from './tfidf/TfIdfForm.vue';

export default {
  name: 'EmbeddingForm',
  props: {
    id: Number,
    embedder_class: null,
    embedder_config: {},
  },
  data() {
    return {
      embedder_class_: null,
      embedder_config_: null,
    };
  },
  components: {
    TransformerEmbedderForm,
    TfIdfForm,
  },
  mounted() {
    this.embedder_class_ = this.embedder_class;
    this.embedder_config_ = this.embedder_config;
  },
  methods: {
    embedderChange() {
      this.embedder_config_ = {};
      this.$emit('embedder-change', {
        embedder_config: this.embedder_config_,
        embedder_class: this.embedder_class_,
      });
      console.log('embedder changed!');
    },
    embedderConfigChange(newConfig) {
      this.embedder_config_ = newConfig;
      this.$emit('embedder-change', {
        embedder_config: this.embedder_config_,
        embedder_class: this.embedder_class_,
      });
    },
  },
};
</script>

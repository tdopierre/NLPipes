<template>
    <b-input-group prepend="Model" class="mb-2">
        <b-form-select
                class=""
                v-model="embedder_config_.model_name_or_path"
                :options="transformers"
                required
                @change="configChange"
        >
        </b-form-select>
    </b-input-group>
</template>

<script>
import $ from 'jquery';

export default {
  name: 'TransformerEmbedderForm',
  props: {
    embedder_config: {
      type: Object,
      default() {
        return {
          model_name_or_path: null,
        };
      },
    },
  },
  data() {
    return {
      transformers: null,
      embedder_config_: {},
    };
  },
  mounted() {
    const that = this;
    $.get(import.meta.env.VITE_SERVER_ADDRESS + '/embedders/transformers', function (response) {
      that.transformers = response;
    }.bind(this));
    this.embedder_config_ = this.embedder_config;
  },
  methods: {
    configChange() {
      this.$emit('embedder-config-change', this.embedder_config_);
    },
  },
};
</script>

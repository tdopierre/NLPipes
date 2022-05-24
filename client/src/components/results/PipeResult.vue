<template>
  <div class="flex flex-col h-screen">
    <div class="p-2 flex items-center bg-gray-50 border-b-4 border-gray-500">
      <b-link
          to="/runs"
          class="hover:bg-gray-200 px-3 py-2 rounded-md cursor-pointer"
          router-tag="span">
        Runs
      </b-link>
      <div class="px-3 py-2 "> ></div>
      <b-link
          :to="'/result/'+thread_id"
          class="hover:bg-gray-200 px-3 py-2 rounded-md cursor-pointer"
          router-tag="span">
        {{ mainProcessConfig.name }}
      </b-link>
      <div class="px-3 py-2 "> ></div>
      <div class="text-gray-900 text-xl font-bold px-3 py-2 ">{{ pipe_name }}</div>
    </div>
    <div>
      <div v-if="this.loading" class="loader bg-gray-400 rounded-full animate-pulse">
      </div>
      <div v-if="!this.loading">
        <Cluster :resultData="this.result_data" v-if="this.result_type==='clusters'"></Cluster>

        <SentimentAnalysis :resultData="this.result_data"
                           v-if="this.result_type==='sentiment_analysis'"></SentimentAnalysis>
        <ClassifierPrediction :resultData="this.result_data"
                              v-if="this.result_type==='classifier_prediction'"></ClassifierPrediction>
        <TrainedModel :resultData="this.result_data" v-if="this.result_type==='trained_model'"></TrainedModel>
      </div>
    </div>
  </div>
</template>


<script>
import $ from 'jquery';
import Cluster from '../Cluster';
import SentimentAnalysis from './SentimentAnalysis';
import ClassifierPrediction from "./ClassifierPrediction";
import TrainedModel from "./TrainedModel";

export default {
  name: 'Result',
  props: {
    thread_id: String,
    pipe_id: String
  },
  data() {
    return {
      allowedTabs: ["clusters", "sentiment_analysis", "classifier_prediction", "trained_model"],
      config: {
        type: Object
      },
      mainProcessConfig: {
        type: Object
      },
      result: {
        type: Object
      },
      pipe_name: "",
      loading: true
    };
  },
  computed: {},
  methods: {
    getMainProcessConfig() {
      const url = import.meta.env.VITE_SERVER_ADDRESS + '/config/' + this.thread_id;
      const that = this;
      $.get(url)
          .then(response => {
            console.log('received', response);
            that.mainProcessConfig = response.config;
          })
          .catch(error => {
            console.log(error);
          });
    },
    getResult() {
      const url = import.meta.env.VITE_SERVER_ADDRESS + '/result/' + this.thread_id + '/' + this.pipe_id;
      const that = this;
      $.get(url)
          .then(response => {
            console.log('received', response);
            that.result_data = response.result_data;
            that.result_type = response.result_type;
            that.pipe_name = response.pipe_name;
            that.loading = false;
          })
          .catch(error => {
            console.log(error);
          });
    },
  },
  mounted() {
    this.getResult();
    this.getMainProcessConfig()
  },
  components: {Cluster, SentimentAnalysis, TrainedModel, ClassifierPrediction},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.loader {
  width: 32px;
  height: 32px;
  position: absolute;
  top: 50%;
  left: 50%;
}

</style>

<template>
  <div>
    <div class="flex flex-col h-screen">
      <div class="p-2 flex items-center bg-gray-50 border-b-4 border-gray-500">
        <b-link to="/runs" class="hover:bg-gray-200 px-3 py-2 rounded-md cursor-pointer" router-tag="span">Runs</b-link>
        <div class="px-3 py-2 "> ></div>
        <div class="text-gray-900 text-xl font-bold px-3 py-2 ">{{ config.name }}</div>
      </div>
      <div class="flex flex-grow overflow-auto justify-left">
        <nav id="" class="w-1/6 relative bg-gray-200 h-full p-3">
          <div class="px-3 py-2 mb-3 rounded-lg cursor-pointer bg-gray-300 tab-link"
               @click="openTab($event, 'content-'+res.pipe.name)"
               v-for="(res, resIndex) in displayableResults"
               v-bind:key="'res-'+resIndex"
          >
            {{ res.pipe.name }}
          </div>
        </nav>
        <div
            class="w-full tab-content overflow-auto"
            :id="'content-'+res.pipe.name"
            v-for="(res, resIndex) in displayableResults"
            v-bind:key="'res-'+resIndex"
        >
          <Cluster :resultData="res.result_data" v-if="res.result_type==='clusters'"></Cluster>

          <SentimentAnalysis :resultData="res.result_data"
                             v-if="res.result_type==='sentiment_analysis'"></SentimentAnalysis>
          <ClassifierPrediction :resultData="res.result_data"
                                v-if="res.result_type==='classifier_prediction'"></ClassifierPrediction>
          <TrainedModel :resultData="res.result_data" v-if="res.result_type==='trained_model'"></TrainedModel>
        </div>
      </div>


    </div>
  </div>
</template>


<script>
import $ from 'jquery';
import Cluster from './Cluster';
import SentimentAnalysis from './results/SentimentAnalysis';
import ClassifierPrediction from "./results/ClassifierPrediction";
import TrainedModel from "./results/TrainedModel";

export default {
  name: 'Result',
  props: {
    thread_id: String,
  },
  data() {
    return {
      result: [],
      allowedTabs: ["clusters", "sentiment_analysis", "classifier_prediction", "trained_model"],
      config: {
        type: Object
      }
    };
  },
  computed: {
    displayableResults() {
      return this.result.filter(res => {
        return this.allowedTabs.includes(res.result_type)
      })
    }
  },
  methods: {
    openTab(evt, tabName) {
      // Get all elements with class="tabcontent" and hide them
      document.getElementsByClassName("tab-content").forEach(el => {
        el.style.display = "none"
      });

      // Get all elements with class="tablinks" and remove the class "active"
      document.getElementsByClassName("tab-link").forEach(el => {
        el.classList.remove("active")
      });

      // Show the current tab, and add an "active" class to the button that opened the tab
      document.getElementById(tabName).style.display = "block";
      console.log('evt', evt)
      evt.target.classList.add("active");
    },
    getResults() {
      const url = import.meta.env.VITE_SERVER_ADDRESS + '/result/' + this.thread_id;
      const that = this;
      $.get(url)
          .then(response => {
            console.log('received', response);
            that.result = response.result;
            that.config = response.config;
          })
          .catch(error => {
            console.log(error);
          });
    },
  },
  mounted() {
    this.getResults();
    console.log('result:', this.result);
  },
  components: {
    ClassifierPrediction,
    SentimentAnalysis,
    Cluster,
    TrainedModel
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.fill {
  min-height: 100%;
  height: 100%;
}

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

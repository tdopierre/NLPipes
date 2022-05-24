<template>
  <div class="flex flex-col h-screen">
      <div class="p-2 flex items-center bg-gray-50 border-b-4 border-gray-500">
        <b-link to="/runs" class="hover:bg-gray-200 px-3 py-2 rounded-md cursor-pointer" router-tag="span">Runs</b-link>
        <div class="px-3 py-2 "> ></div>
        <div class="text-gray-900 text-xl font-bold px-3 py-2 ">{{ config.name }}</div>
      </div>
    <network ref="network" class="w-100 h-100"
                             :nodes="graph.nodes"
                             :edges="graph.edges"
                             :options="graph.options"
                             @select-node="selectNode"


                    v-if="this.config !== undefined">
    </network>
  </div>
</template>


<script>
import $ from 'jquery';
// import Cluster from './Cluster';
// import SentimentAnalysis from './results/SentimentAnalysis';
// import ClassifierPrediction from "./results/ClassifierPrediction";
// import TrainedModel from "./results/TrainedModel";

export default {
  name: 'Result',
  props: {
    thread_id: String,
  },
  data() {
    return {
      allowedTabs: ["clusters", "sentiment_analysis", "classifier_prediction", "trained_model"],
      config: {
        type: Object
      }
    };
  },
  computed: {
    graph() {
      if (this.config.pipe_configs === undefined) {
        return {
          nodes: [],
          edges: []
        }
      }
      var graph = {
        nodes: [],
        edges: [],
        options: {
          nodes: {
            shape: 'dot',
            size: 15,
            borderWidth: 1,
            font: {
              face: 'monospace',
              align: 'left',
              size: 12,
            },
          },
          edges: {
            color: '#656765',
          },
          layout: {
            randomSeed: 42,
          },

        },
      };

      this.config.pipe_configs.forEach(pipe => {
        graph.nodes.push({
          id: pipe.id,
          label: pipe.name,
          shape: 'dot',
        });
      });
      this.config.pipe_configs.forEach(pipe => {
        if ('dependencies' in pipe) {
          pipe.dependencies.forEach(dep => {
            graph.edges.push({
              from: dep,
              to: pipe.id,
              arrows: 'to',
            });
          });
        }
      });
      return graph;
    }
  },
  methods: {
    getConfig() {
      const url = import.meta.env.VITE_SERVER_ADDRESS + '/config/' + this.thread_id;
      const that = this;
      $.get(url)
          .then(response => {
            console.log('received', response);
            that.config = response.config;
          })
          .catch(error => {
            console.log(error);
          });
    },
    selectNode(node) {
      console.log('selected node', node)
      this.$router.push("/result/"+this.thread_id+'/'+node.nodes[0])
    }
  },
  mounted() {
    this.getConfig();
    console.log('config:', this.config);
  },
  components: {

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

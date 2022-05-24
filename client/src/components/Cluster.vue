<template>
  <div class="p-3">
    <div class=" m-auto">

          <div class="flex-wrap">
            <div
                v-for="(cluster, clusterIndex) in this.clusters"
                class="mb-3 border-solid border-2 rounded-lg border-gray-800"
                :id="'cluster'+(clusterIndex)"
                v-bind:key="'cluster-'+clusterIndex"
            >

              <!--header-->
              <div class="bg-gray-700 p-3">
                <div class=" d-flex flex-nowrap items-center" style="justify-content: space-between">
                  <div>
                    <span class="text-lg text-gray-200">#{{ (cluster.id) }}</span>
                  </div>
                  <div class="w-2/3">
                    <b-badge v-for="(topic, topicIx) in cluster.topics"
                             v-bind:key="'cluster-'+clusterIndex+'-topic-'+topicIx"
                             class=" bg-gray-100 text-black py-1 px-2 rounded mx-2"
                    >{{ topic }}
                    </b-badge>
                  </div>
                  <div>
                    <span class="p-2 border-2 border-gray-200 rounded-xl text-gray-200">{{
                        cluster.items.length + ' items'
                      }}
                    </span>
                  </div>
                </div>
              </div>
              <!-- content -->
              <div class="p-0 card-body" style="max-height: 30vh; height:auto; overflow-y: scroll">

                <div v-for="(item, itemIndex) in cluster.items.slice(0, displayLimit)"
                     class="cluster-sample hover:bg-gray-200 py-1 px-3" style="overflow-wrap: break-word"
                     v-bind:key="'cluster-'+clusterIndex+'-item-'+itemIndex"
                >
                  <div>{{ item.text }}</div>

                </div>
                <div v-if="cluster.items.length > displayLimit">
                  ...
                </div>
              </div>
            </div>
          </div>
        </div>



  </div>
</template>


<script>
// var Plotly = require('plotly.js-dist');
import Plotly from 'plotly.js-dist';

class DataSample {
  constructor({text, embedding_2d = null}) {
    this.text = text;
    this.embedding_2d = embedding_2d;
  }
}

class Cluster {
  constructor({id, topics = [], representative = null, items = [], avgDistanceToCentroid = null}) {
    this.id = id
    this.topics = topics
    this.representative = representative
    this.avgDistanceToCentroid = avgDistanceToCentroid
    this.items = items
  }

  addItem(item) {
    this.items.push(item)
  }
}


export default {
  name: 'Cluster ',
  props: {
    resultData: {
      type: Object
    },
  },
  data() {
    return {
      displayLimit: 999,
      clusters: []
    };
  },
  mounted() {
    // Create clusters
    this.resultData.clusters_info.forEach((clusterInfo, clusterIx) => {
      this.clusters.push(new Cluster({
            id: clusterIx,
            topics: clusterInfo.topics,
            representative: new DataSample(clusterInfo.representative),
            avgDistanceToCentroid: clusterInfo.avg_distance_to_centroid,
            items: []
          })
      )
    })
    console.log('Received clusters', this.clusters)

    // Add items to clusters
    this.resultData.dataset.forEach(item => {
      this.clusters[item.cluster].addItem(new DataSample(item))
    })
    console.log('Items added to clusters')
    this.clusters.sort(function (a, b) {
      return a.avgDistanceToCentroid - b.avgDistanceToCentroid

    });

    var traces = [];
    this.clusters.forEach((cluster, clusterIx) => {
      var trace = {
        x: [],
        y: [],
        text: [],
        makers: {
          size: 100,
        },
        mode: 'markers',
        type: 'scatter',
        name: 'Cluster ' + (clusterIx + 1),
      };
      cluster.items.forEach((clusterItem) => {
        trace.x.push(clusterItem.embedding_2d[0]);
        trace.y.push(clusterItem.embedding_2d[1]);
        trace.text.push(clusterItem.text);
      });
      traces.push(trace);
    });
    console.log('plotting traces', traces);
    Plotly.newPlot('plot', traces);
  },
}
;
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.cluster-sample {
  /*text-overflow: ellipsis;*/
  /*height: 1.2em;*/

}

/* width */

</style>

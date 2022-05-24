<template>
  <div>
    <div class="p-4 bg-white block sm:flex items-center justify-between border-b border-gray-200 lg:mt-1.5">
      <div class="mb-1 w-full">
        <div class="mb-4">
          <h1 class="text-xl sm:text-2xl font-semibold text-gray-900">All runs</h1>
        </div>
        <div class="sm:flex">
          <div class="hidden sm:flex items-center sm:divide-x sm:divide-gray-100 mb-3 sm:mb-0">
            <form class="lg:pr-3" action="#" method="GET">
              <label for="users-search" class="sr-only">Search</label>
              <div class="mt-1 relative lg:w-64 xl:w-96">
                <input type="text" name="email" id="users-search"
                       class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5"
                       placeholder="Search for a run" v-model="searchRunsQuery">
              </div>
            </form>
          </div>
          <div class="flex items-center space-x-2 sm:space-x-3 ml-auto">
            <button type="button" v-b-modal.modal-new-process-suggest
                    class="w-1/2 text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 font-medium inline-flex items-center justify-center rounded-lg text-sm px-3 py-2 text-center sm:w-auto">
              <svg class="-ml-1 mr-2 h-6 w-6" fill="currentColor" viewBox="0 0 20 20"
                   xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                      d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                      clip-rule="evenodd"></path>
              </svg>
              New run
            </button>

          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col">
      <div class="overflow-x-auto">
        <div class="align-middle inline-block min-w-full">
          <div class="shadow overflow-hidden">
            <table class="table-fixed w-full divide-y divide-gray-200">
              <thead class="bg-gray-100">
              <tr>
                <th scope="col" class="p-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Name
                </th>
                <th scope="col" class="p-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Status
                </th>
                <th scope="col" class="p-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Actions
                </th>
                <!--                <th scope="col" class="p-3 text-left text-xs font-medium text-gray-500 uppercase">-->

                <!--                </th>-->

              </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
              <tr class="hover:bg-gray-100" v-for="(run) in filteredRunsBySearch" v-bind:key="run.id">
                <td class="p-3 whitespace-nowrap text-base font-normal text-gray-900">
                  <div class="text-sm font-normal text-gray-500">
                    <div class="text-base font-bold text-gray-900">{{ run.name }}</div>
                  </div>
                </td>
                <td class="p-3 whitespace-nowrap text-base font-normal text-gray-900">
                  <div class="flex items-center">
                    <div v-bind:class="{
                      'bg-green-400': run.status.toLowerCase().includes('complete'),
                      'bg-red-400': run.status.toLowerCase().includes('error'),
                    }" class="h-2.5 w-2.5 rounded-full mr-2 bg-yellow-400"></div>
                    {{ run.status }}
                  </div>
                </td>
                <td class="p-3 whitespace-nowrap space-x-2">
                  <b-button class="mr-1" size="sm" @click="toggleModalProgress(run.id)">
                    <div class="flex items-center text-sm">
                      <div><i class="fas fa-project-diagram"></i></div>
                      <!--                      <div class="ml-2 text-sm">Structure</div>-->
                    </div>
                  </b-button>
                  <b-button class="mx-1" size="sm"
                            v-if="run.status.toLowerCase()==='complete'"
                            variant="primary"
                            :href="'http://10.200.130.43:8001'+'/result/download'"
                            @click.prevent="downloadItem({id:run.id, label:'clusters.json'})"
                  >
                    <div class="flex items-center text-sm">
                      <div><i class="fas fa-download"></i></div>
                      <!--                      <div class="ml-2 text-sm">Download</div>-->
                    </div>
                  </b-button>

                  <!--view-->
                  <router-link
                      v-if="run.status.toLowerCase()==='complete'"
                      :to="'/result/'+run.id"
                      class="m-0"
                  >
                    <b-button class="mx-1" size="sm"
                              v-if="run.status.toLowerCase()==='complete'"
                              variant="success"
                              :href="'http://10.200.130.43:8001'+'/result/download'"
                    >
                      <div class="flex items-center text-sm">
                        <div><i class="fas fa-poll"></i></div>
                        <!--                      <div class="ml-2 text-sm">Results</div>-->
                      </div>
                    </b-button>
                  </router-link>
                  <b-button class="mx-1" size="sm" @click="deleteProcess(run.id)" variant="danger">
                    <div class="flex items-center text-sm">
                      <div><i class="fas fa-trash"></i></div>
                      <!--                      <div class="ml-2 text-sm">Delete</div>-->
                    </div>
                  </b-button>
                  <!--                  <b-button class="mr-1" size="sm" @click="toggleRunProgress(run.id)">-->
                  <!--                    <div class="flex items-center text-sm">-->
                  <!--                      <div><i class="fas fa-project-diagram"></i></div>-->
                  <!--                      &lt;!&ndash;                      <div class="ml-2 text-sm">Structure</div>&ndash;&gt;-->
                  <!--                    </div>-->
                  <!--                  </b-button>-->
                </td>
                <!--                <td class="w-1/6 whitespace-nowrap space-x-2">-->
                <!--                  <div style="width:400px" >-->
                <!--                    <div style="height:200px" :id="'process-graph-'+run.id" class="hidden">-->
                <!--                      <ProcessGraph-->
                <!--                          :pipes="run.pipe_configs"-->
                <!--                      ></ProcessGraph>-->
                <!--                    </div>-->
                <!--                  </div>-->
                <!--                </td>-->
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div class="" style="text-align: left">
      <div>
        <b-modal id="modal-process-progress" :title="selectedRunConfig.name+ ' - Progress'" hide-footer size="lg"
                 centered
                 :hidden="this.selectedRunConfig === null">
          <div class="card p-0 w-full m-auto" style="height:500px; border-color: #1f2020">

            <ProcessGraph
                :pipes="this.selectedRunConfig.pipe_configs"
            ></ProcessGraph>


          </div>

        </b-modal>

      </div>
      <div>
        <b-modal id="modal-new-process-suggest" title="New Process" hide-footer size="xl" centered
        >
          <div style="justify-content: space-around" class="d-flex flex-wrap p-0">
            <div class="max-w-md py-4 px-4 shadow rounded-lg my-2 hover:bg-gray-100 cursor-pointer"
                 style="width:32%"
                 v-for="(config, configIx) in predefinedConfigs" v-bind:key="'config-'+configIx"
                 @click="setNewPredefinedConfig(config.pipes)">
              <div>
                <div class="text-gray-800 text-sm font-semibold">{{ config.title }}</div>
                <p class="mt-2 text-gray-600 text-sm">{{ config.description }}</p>
              </div>

            </div>
          </div>

        </b-modal>
      </div>
      <div>
        <b-modal id="modal-new-process-edit" title="New Process" hide-header hide-footer size="xl" centered>
          <div class="p-1">
            <div class="">
              <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-last-name">
                new run
              </label>
              <input
                  class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                  id="grid-last-name" type="text" placeholder="Run name..." v-model="newRun.name" required>
            </div>
            <div class="flex my-2" >

              <div class="w-1/2 mr-1">
                <b-card v-if="this.newRun.activePipe.pipe_type !== undefined" class="border-1 border-gray-500" style="min-height: 500px">
                  <b-card-text class="m-auto p-0">
                    <div class="w-full">
                      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
                             for="grid-last-name">
                        Block Name
                      </label>
                      <input
                          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-2 px-2 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                          type="text" v-model="newRun.activePipe.name">
                    </div>
                    <!--                      <b-form-group-->
                    <!--                          id="new-pipe-name"-->
                    <!--                          label="Name"-->
                    <!--                          label-for="new-pipe-name-input"-->
                    <!--                          class="m-2"-->
                    <!--                      >-->
                    <!--                        <b-input-group id="new-pipe-name-input">-->
                    <!--                          <b-input v-model="newRun.activePipe.name"></b-input>-->
                    <!--                        </b-input-group>-->
                    <!--                      </b-form-group>-->


                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 mt-3">
                      Dependencies
                    </label>
                    <multiselect
                        v-model="newRun.activePipe.dependencies"
                        :options="availablePipes"
                        :multiple="true"
                        :custom-label="pipeIdToName"
                        :disabled="availablePipes.length <= 1"
                        class=""
                    >
                      <template
                          slot="option"
                          slot-scope="props">
                        <div class="option__desc"><span class="option__title">{{
                            pipeIdToName(props.option)
                          }}</span><span
                            class="option__small">{{ props.option.desc }}</span></div>
                      </template>
                    </multiselect>


                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 mt-3">
                      Type
                    </label>
                    <select
                        class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-2 px-2 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                        id="grid-state" v-model="newRun.activePipe.pipe_type" required
                        @change="newRun.activePipe.config = {}">
                      <option v-for="option in pipeTypes" v-bind:key="'pipeType-option-'+option">{{ option }}</option>

                    </select>


                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 mt-3">
                      Config
                    </label>
                    <FileForm
                        v-if="newRun.activePipe.pipe_type==='file_reader'"
                        v-bind:form="newRun.activePipe.config"
                        v-on:file-change="newRun.activePipe.config=$event"
                    ></FileForm>
                    <!--                                                        v-on:file-change="newRun.activePipe.config=$event"-->

                    <EmbeddingForm
                        v-if="newRun.activePipe.pipe_type==='embedding'"
                        :embedder_config="newRun.activePipe.config.embedder_config"
                        :embedder_class="newRun.activePipe.config.embedder_class"
                        v-on:embedder-change="newRun.activePipe.config=$event"
                    />
                    <ClusteringForm
                        v-if="newRun.activePipe.pipe_type==='clustering'"
                        :model_class="newRun.activePipe.config.model_class"
                        :model_config="newRun.activePipe.config.model_config"
                        v-on:model-change="newRun.activePipe.config=$event"
                    />
                    <!--                                                        :model_class="newRun.activePipe.config.model_class"-->
                    <!--                                                        :model_config="newRun.activePipe.config.model_config"-->
                    <SentimentAnalysisForm
                        v-if="newRun.activePipe.pipe_type==='sentiment_analysis'"
                        v-on:change="newRun.activePipe.config=$event"
                    />

                    <b-button
                        variant="danger" class="w-100 m-auto"
                        @click="deletePipe(newRun.activePipe.id)"
                    >
                      <!--:disabled="pipe.pipe_type==='file_reader'"-->
                      Delete Pipe
                    </b-button>
                  </b-card-text>
                </b-card>
              </div>
              <div class="w-1/2 ml-1">
                <div class="card w-100 bg-gray-100" style="height:500px; border-color: #6c6c6c">
                  <div id="graph" style="border-color: red">
                    <network ref="network" class="w-100 h-100"
                             :nodes="graph.nodes"
                             :edges="graph.edges"
                             :options="graph.options"
                             @select-node="selectNode"
                             @deselect-node="deselectNode"
                    >
                    </network>
                  </div>
                </div>
              </div>


            </div>
            <div class="w-full flex">
              <b-button @click="newPipe" class="w-1/2 mr-1">Add Pipe</b-button>
              <b-button variant="primary" class="w-1/2 ml-1" @click="onSubmit">Run</b-button>

            </div>
          </div>
        </b-modal>
      </div>


    </div>
  </div>
</template>

<script>

import axios from 'axios';
import $ from 'jquery';
import {v4 as uuidv4} from 'uuid';
import FileForm from './newPipe/file/FileForm';
import ClusteringForm from './newPipe/clustering/ClusteringForm';
import EmbeddingForm from './newPipe/embedding/EmbeddingForm';
import SentimentAnalysisForm from './newPipe/sentiment_analysis/SentimentAnalysisForm';
import ProcessGraph from './viz/ProcessGraph';
import {getProcessConfig, predefinedConfigs} from '../pipe_configs.js';
import Multiselect from 'vue-multiselect'

console.log('getProcessConfig', getProcessConfig);

export default {
  name: 'Main',
  data() {
    return {
      searchRunsQuery: '',
      predefinedConfigs: predefinedConfigs,
      selectedRunConfig: {
        pipes: []
      },
      newRun: {
        name: null,
        id: uuidv4(),
        tabIndex: 0,
        pipes: [
          {
            id: uuidv4(),
            pipe_type: 'file_reader',
            name: 'File Reader',
            config: {
              file_type: 'txt',
            },
            dependencies: [],
          },
        ],
        activePipe: {},
      },
      pipeTypes: [
        'file_reader',
        'embedding',
        'clustering',
        'sentiment_analysis',
      ],
      fields: [
        {
          'key': 'name',
          'label': 'Name',
          'sortable': 'true',
        },
        {
          'key': 'status',
          'label': 'Status',
        },
        {
          'key': 'actions',
          'label': 'Actions',
        },
      ],
      runs: [],
    };
  },
  computed: {
    filteredRunsBySearch: function () {
      if (this.searchRunsQuery === '') {
        return this.runs
      }
      return this.runs.filter(run => (run.name.toLowerCase().indexOf(this.searchRunsQuery.toLowerCase()) >= 0))
    },
    graph() {
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

      this.newRun.pipes.forEach(pipe => {
        graph.nodes.push({
          id: pipe.id,
          label: pipe.name,
          shape: 'dot',
        });
      });
      this.newRun.pipes.forEach(pipe => {
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
    },
    availablePipes() {
      let availablePipes = [];
      this.newRun.pipes.forEach(pipe => {
        availablePipes.push(pipe.id);
      });
      return availablePipes;
    },
  },
  methods: {
    toggleRunProgress(runId) {
      let el = document.getElementById('process-graph-' + runId);
      if (el.classList.contains("hidden")) {
        el.classList.remove("hidden")
      } else {
        el.classList.add("hidden")
      }
    },
    setNewPredefinedConfig(pipes) {
      let newPipes;
      if (pipes != null) {
        newPipes = pipes;
      } else {
        newPipes = [
          {
            id: uuidv4(),
            pipe_type: 'file_reader',
            name: 'File Reader',
            config: {
              file_type: 'txt',
            },
            dependencies: [],
          },
        ];

      }
      console.log('setting pipes to', JSON.stringify(newPipes, null, 2));
      this.newRun.pipes = newPipes;
      // if (this.newRun.pipes.length > 0) {
      //   this.setActivePipe(this.newRun.pipes[0].id);
      // }
      this.$bvModal.hide('modal-new-process-suggest');
      this.$bvModal.show('modal-new-process-edit');
      this.unsetActivePipe();
      this.newRun.id = uuidv4();

    },
    deleteProcess(id) {
      const url = import.meta.env.VITE_SERVER_ADDRESS + '/processes/' + id;
      $.ajax({
        url: url,
        type: 'DELETE',
        success: function () {
          console.log('deleted process with id', id, 'successfully');
        },
        error: console.error,

      });
    },
    setActivePipe(id) {
      console.log('asked to set', id, 'active');
      this.newRun.pipes.forEach(pipe => {
        if (pipe.id === id) {
          this.newRun.activePipe = pipe;
          console.log('setting new active', pipe);
        }
      });
    },
    deletePipe(id) {
      this.newRun.pipes.forEach(((pipe, index) => {
        pipe.dependencies.forEach((dep, index2) => {
          if (dep === id) {
            this.newRun.pipes[index].dependencies.splice(index2, 1);
          }
        });
        if (pipe.id === id) {
          this.newRun.pipes.splice(index, 1);
        }
      }));
      this.unsetActivePipe()
      // if (this.newRun.pipes.length > 0) {
      //   this.setActivePipe(this.newRun.pipes[this.newRun.pipes.length - 1].id);
      // }
    },
    pipeIdToName(id) {
      console.debug('Looking for pipe with id', id);
      const found = this.newRun.pipes.find(element => {
        console.debug('in `pipeIdToName`, looking at element', element)
        return element.id === id;
      });
      return found.name;
    },
    unsetActivePipe() {
      console.debug("Unsetting active pipe")
      this.newRun.activePipe = {};
    },
    deselectNode(event) {
      console.log('deselected node with event', event)
      this.unsetActivePipe()
    },
    selectNode(event) {
      const id = event.nodes[0];
      // console.log('selectNode', event, 'id', id);
      this.unsetActivePipe();
      this.setActivePipe(id);
      this.newRun.pipes.forEach((pipe, index) => {
        if (pipe.id === id) {
          this.newRun.tabIndex = index;
        }
      });
    },
    toggleModalProgress(id) {
      this.runs.forEach((run) => {
        if (run.id === id) {
          this.selectedRunConfig = run;
          console.log('just set selected run to', run)
        }
      });
      this.$bvModal.show('modal-process-progress');
    },
    cancelRun(id) {
      console.log('cancelling', id);
      const url = import.meta.env.VITE_SERVER_ADDRESS + '/process/' + id;
      $.delete(url);
    },
    newPipe() {

      const id = uuidv4();
      this.newRun.pipes.push({
        name: '<NewPipe>',
        id: id,
        pipe_type: '',
        config: {},
        dependencies: [],
      });
      this.setActivePipe(id);
    },
    downloadItem({id, label}) {
      console.log('I\'m asked to download item with id', id, label);
      const url = import.meta.env.VITE_SERVER_ADDRESS + '/result/' + id;
      $.get(url)
          .then(response => {
            console.log('response:', response);
            const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(response, null, 2));
            const link = document.createElement('a');
            link.href = dataStr;
            link.download = label;
            link.click();
            URL.revokeObjectURL(link.href);
          })
          .catch(console.error);
    },

    onSubmit() {


      /* Initialize the form data */
      const formData = new FormData();

      /* Add input file(s) */
      this.newRun.pipes.forEach(element => {
        console.log('pipe', element);
        if (element.pipe_type === 'file_reader') {
          console.log('cfg', element.config);
          console.log('file', element.file);
          formData.append(element.id, element.config.file);
        }
      });

      /* Add pipes */
      formData.append('name', this.newRun.name);
      formData.append('id', this.newRun.id);
      const pipes = JSON.stringify(this.newRun.pipes);
      formData.append('pipes', pipes);

      console.log(formData);

      /* Send new process to the backend */
      axios
          .post(import.meta.env.VITE_SERVER_ADDRESS + '/process', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then(() => {
            // that.runs.push(resp.data);
            this.$bvModal.hide('modal-new-process-edit');
            // clearTimeout(refreshProcessesTimeout);
            // this.refreshProcesses();
            console.log('SUCCESS!!');
          })
          .catch(() => {
            console.log('FAILURE!!');
          });
    },
    refreshProcesses() {
      console.log('refreshing processes');
      $.get(import.meta.env.VITE_SERVER_ADDRESS + '/processes', function (response) {
        if (this.runs.length === 0) {
          this.runs = response;
        } else {
          response.forEach((resp) => {
            this.runs.forEach((run) => {
              if (resp.id === run.id) {
                run.status = resp.status;
              }
            });
          });
        }
      }.bind(this));

    },
  },
  mounted() {

    const that = this;
    $.get(import.meta.env.VITE_SERVER_ADDRESS + '/embedders', function (response) {
      that.embedders = response;
    }.bind(this));

    $.get(import.meta.env.VITE_SERVER_ADDRESS + '/models', function (response) {
      that.models = response;
    }.bind(this));

    this.refreshProcesses();

    this.newRun.activePipe = this.newRun.pipes[0];
  },
  sockets: {
    'progress-update': function (data) {
      const id = data.id;
      const status = data.status;
      this.runs.forEach(run => {
        if (run.id === id) {
          run.status = status;
        }
        run.pipe_configs.forEach(pipe_config => {
          if (pipe_config.id === id) {
            pipe_config.status = status;
          }
        });
      });
      console.info('progress-update', data);
    },
    'new-process': function (data) {
      this.runs.unshift(data);
    },
    'delete-process': function (data) {
      this.runs.forEach((run, runIndex) => {
        if (run.id === data.id) {
          this.runs.splice(runIndex, 1);
        }
      });
    },
  },
  components: {
    ProcessGraph,
    SentimentAnalysisForm,
    FileForm,
    EmbeddingForm,
    ClusteringForm,
    Multiselect,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
.multiselect__select, .multiselect__placeholder, .multiselect__tags, .multiselect__input {
  @apply bg-gray-200;
}

.multiselect__tag {
  @apply my-0;
  @apply mr-1;
  @apply bg-gray-400;
}

.multiselect__tag-icon:hover {
  @apply bg-red-500;
  @apply text-white;
}

.multiselect__tag-icon:after {
  @apply text-gray-700;
  transition: ease .2s;
}

.multiselect__select {
  transition: none;
}
canvas {
  height: 100px;
  width: 100px;
}

#graph {
  height: 100%;
  width: 100%;
}

ul {
  display: none
}


/*.multiselect__select, .multiselect__placeholder, .multiselect__tags, .multiselect__input{*/
/*  @apply bg-gray-200;*/
/*}*/

.mutliselect__tag {
  margin-bottom: 0
}

.multiselect__input {
  @apply text-red-500
}

</style>

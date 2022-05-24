<template>
  <div>
    <div class="px-4 py-2 bg-white block sm:flex items-center justify-between border-b border-gray-200 lg:mt-1.5">
      <div class="mb-1 w-full">

        <div class="sm:flex items-center justify-between">
            <div class="text-xl sm:text-xl font-semibold text-gray-900 ">
              Sentiment Analysis
            </div>



          <jw-pagination :items="filteredRunsBySearch" :labels="paginationCustomLabels" :maxPages="3" @changePage="onChangePage" :pageSize="perPage"></jw-pagination>
          <form class="" action="#" method="GET">
            <label for="users-search" class="sr-only">Search</label>
            <div class=" relative lg:w-64 xl:w-96">
              <input type="text" name="email" id="users-search"
                     class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2"
                     placeholder="Search..." v-model="searchQuery">
            </div>
          </form>
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
                <th
                    scope="col"
                    class="p-3 text-left text-xs font-medium text-gray-500 uppercase cursor-pointer col-name"
                    id="col-id"
                    @click="toggleSorting('id')"
                    style="width: 5%"
                >
                  #
                  <i class="fa fa-arrow-up text-xs ml-1 sorting-arrow hidden"></i>
                  <i class="fa fa-arrow-down text-xs ml-1 sorting-arrow hidden"></i>
                </th>
                <th scope="col" class="w-1/2 p-3 text-left text-xs font-medium text-gray-500 uppercase cursor-pointer col-name" id="col-text" @click="toggleSorting('text')">
                  Texts
                  <i class="fa fa-arrow-up text-xs ml-1 sorting-arrow hidden"></i>
                  <i class="fa fa-arrow-down text-xs ml-1 sorting-arrow hidden"></i>
                </th>
                <th scope="col" class="w-1/12 p-3 text-left text-xs font-medium text-gray-500 uppercase cursor-pointer col-name" id='col-score' @click="toggleSorting('score')">
                  Sentiment Score
                  <i class="fa fa-arrow-up text-xs ml-1 sorting-arrow hidden"></i>
                  <i class="fa fa-arrow-down text-xs ml-1 sorting-arrow hidden"></i>
                </th>
                <th scope="col" class="w-1/6 p-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Sentiment Categories
                </th>
                <!--                <th scope="col" class="p-3 text-left text-xs font-medium text-gray-500 uppercase">-->

                <!--                </th>-->

              </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
              <tr class="hover:bg-gray-100" v-for="(item) in pageOfDataset" v-bind:key="item.id">
                <td class="p-1 px-3 whitespace-nowrap text-base font-normal text-gray-900">
                  <div class="text-sm font-normal text-gray-500">
                    <div class="text-base text-gray-900">{{ item.id }}</div>
                  </div>
                </td>
                <td class="p-1 px-3 text-base font-normal text-gray-900" style="white-space: initial">
                  <div class="text-sm font-normal text-gray-500">
                    <div class="text-base text-gray-900">{{ item.text }}</div>
                  </div>
                </td>
                <td class="p-1 px-3 whitespace-nowrap text-base font-normal text-gray-900">
                  <div class="flex items-center">
                    <div class="text-base text-gray-900">{{ item.score }}</div>
                  </div>
                </td>
                <td class="p-1 px-3 whitespace-nowrap text-base font-normal text-gray-900">
                  <div class="items-center">
                    <b-progress max="1">
                      <b-progress-bar
                          v-for="sentimentIx in [0, 1, 2, 3, 4]"
                          v-bind:key="sentimentIx"
                          :value="item.scoreArray[sentimentIx]"
                          :style="{'background-color': colors[sentimentIx]}"
                      ></b-progress-bar>

                      <!--          <b-progress-bar style="background-color: #ff0000"-->
                      <!--                          :value="row.item.sentiment.score_1"></b-progress-bar>-->
                      <!--          <b-progress-bar style="background-color: #ff8b00"-->
                      <!--                          :value="row.item.sentiment.score_2"></b-progress-bar>-->
                      <!--          <b-progress-bar style="background-color: #f7ff00"-->
                      <!--                          :value="row.item.sentiment.score_3"></b-progress-bar>-->
                      <!--          <b-progress-bar style="background-color: #87ff00"-->
                      <!--                          :value="row.item.sentiment.score_4"></b-progress-bar>-->
                      <!--          <b-progress-bar style="background-color: #00ff1f"-->
                      <!--                          :value="row.item.sentiment.score_5"></b-progress-bar>-->
                    </b-progress>

                  </div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import JwPagination from 'jw-vue-pagination';

class DataSampleWithSentiment {
  constructor({text, score, scoreArray, id}) {
    this.text = text;
    this.score = score;
    this.scoreArray = scoreArray;
    this.id = id;
  }
}

const paginationCustomLabels = {
    first: '<<',
    last: '>>',
    previous: '<',
    next: '>'
};

export default {
  name: 'SentimentAnalysis',
  props: {
    resultData: {
      type: Array
    },
  },
  mounted() {
    this.resultData.forEach((sample, sampleIx) => {
      this.dataset.push(new DataSampleWithSentiment({
        text: sample.text,
        score: sample.sentiment.score,
        scoreArray: [
          sample.sentiment.score_1,
          sample.sentiment.score_2,
          sample.sentiment.score_3,
          sample.sentiment.score_4,
          sample.sentiment.score_5
        ],
        id: sampleIx
      }))
    })
    console.log('Filed dataset with', this.dataset.length, 'samples')
    console.log(this.dataset);
  },
  data() {
    return {
      paginationCustomLabels,
      searchQuery: '',
      perPage: 100,
      currentPage: 3,
      dataset: [],
      pageOfDataset: [],
      colors: [
        '#ff0000',
        '#ff8b00',
        '#f7ff00',
        '#87ff00',
        '#00ff1f'
      ],
      fields: [
        {
          key: 'text',
          label: 'Text',
          sortable: false,
        },
        {
          key: 'sentiment.score',
          label: 'Score',
          sortable: false,
        },
        {
          key: 'sentiment',
          label: 'Sentiment',
          sortable: false
        },
      ],
    };
  },
  methods: {
    sortDataset({key, ascending = true}) {
      console.log('Sorting dataset with params', {key: key, ascending: ascending})
      this.dataset.sort(function (a, b) {
        // console.log(a['text'], b['text'], a['text'].localeCompare(b['text']));
        if (typeof (a[key]) === 'string') {
          return a[key].localeCompare(b[key]);
        } else {
          return a[key] - b[key];
        }

      })
      if (!ascending) {
        this.dataset.reverse();
      }
    },
    onChangePage(pageOfItems) {
      // update page of items
      this.pageOfDataset = pageOfItems;
    },
    toggleSorting(key) {
      const el = document.getElementById('col-' + key)

      document.getElementsByClassName('col-name').forEach(element => {
        if (element.id !== 'col-' + key) {
          element.classList.remove('font-bold');
          element.getElementsByClassName('sorting-arrow').forEach(element => {
            element.classList.add('hidden');
          })
        }
      })
      console.log()
      if (el.children[0].classList.contains('hidden') && el.children[1].classList.contains('hidden')) {
        el.classList.add('font-bold');
        el.children[0].classList.remove('hidden');
        this.sortDataset({
          key: key,
          ascending: true
        })
      } else if (el.children[0].classList.contains('hidden')) {
        el.classList.remove('font-bold');
        el.children[0].classList.add('hidden');
        el.children[1].classList.add('hidden');
        this.sortDataset({
          key: 'id',
          ascending: true
        })
      } else if (el.children[1].classList.contains('hidden')) {
        el.children[0].classList.add('hidden');
        el.children[1].classList.remove('hidden');
        this.sortDataset({
          key: key,
          ascending: false
        })
      }
    }
  },
  components: {
    JwPagination
  },
  computed: {
    filteredRunsBySearch: function () {
      if (this.searchQuery === '') {
        return this.dataset
      }
      return this.dataset.filter(item => (item.text.toLowerCase().indexOf(this.searchQuery.toLowerCase()) >= 0))
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
table {
  vertical-align: middle;

}
</style>

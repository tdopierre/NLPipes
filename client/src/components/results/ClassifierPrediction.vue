<template>
  <div>
    <div class="flex overflow-auto">
      <div class="overflow-wrap h-full w-1/2 bg-gray-100 h-auto font-mono" id="labelList">
        <div
            v-for="label in labelMapper.uniqueLabels"
            v-bind:key="label"
            class="px-3 py-1 hover:bg-gray-200 label-name cursor-pointer monospace text-xs items-center flex justify-between"
            :id="'label-'+label"
            @click="selectLabel(label)"
        >
          <div class="font-mono text-sm"> {{ label }}</div>
          <div>[{{ labeledDatasets[label].samples.length }}]</div>
        </div>
      </div>
      <div class="overflow-auto w-1/2 p-2">
        <div v-if="selectedLabel!== null">
          <div
              v-for="sample in labeledDatasets[selectedLabel].samples"
              v-bind:key="'label-'+selectedLabel+'-sample-'+sample.id"
              class="p-2 border-2 mx-2 mb-2 rounded-md flex items-center justify-between border-gray-300"
          >
            <div>{{ sample.text }}</div>
            <b-badge pill class="px-2 py-1">#{{ sample.id }}</b-badge>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
<script>

class LabeledDataset {
  constructor({labelName}) {
    this.labelName = labelName;
    this.samples = [];
  }
}

class PredictedDataSample {
  constructor({text, score = null, prediction = [], id}) {
    this.text = text;
    this.score = score;
    this.prediction = prediction;
    this.id = id;
  }
}

class LabelMapper {
  constructor(uniqueLabels) {
    this.uniqueLabels = uniqueLabels;
    this.uniqueLabels.sort();
    this._labelToIx = {};
    this.uniqueLabels.forEach((label, labelIx) => {
      this._labelToIx[label] = labelIx
    })
    this._ixToLabel = this.uniqueLabels;
  }

  ixToLabel(ix) {
    return this._ixToLabel[ix]
  }

  labelToIx(label) {
    return this._labelToIx[label]
  }
}

export default {
  name: 'ClassifierPrediction',
  props: {
    resultData: {
      type: Array
    }
  },
  methods: {
    selectLabel(label) {
      // Purge all labels
      console.log(label)
      document.getElementById('labelList').children.forEach(child => {
        child.classList.remove("selected")
      })
      document.getElementById('label-' + label).classList.add("selected")
      this.selectedLabel = label;
    }
  },
  data() {
    return {
      testVariable: "testValue",
      labeledDatasets: {},
      samples: [],
      labelMapper: {
        type: LabelMapper
      },
      selectedLabel: null
    }
  },
  mounted() {
    console.log('Found', this.resultData.length, 'samples')
    this.resultData.forEach((sample, sampleIx) => {
      const predictedDataSample = new PredictedDataSample({
        text: sample.text,
        prediction: sample.prediction,
        id: sampleIx + 1,
      })
      //
      this.samples.push(predictedDataSample);
    })
    let allLabels = [];
    this.samples.forEach(sample => {
      sample.prediction.forEach(pred => {
        allLabels.push(pred)
      })
    })
    this.labelMapper = new LabelMapper([...new Set(allLabels)])
    console.debug('Created LabelMapper', this.labelMapper)
    this.samples.forEach(predictedDataSample => {
      predictedDataSample.prediction.forEach(label => {

        if (!(label in this.labeledDatasets)) {
          this.labeledDatasets[label] = new LabeledDataset({
            labelName: label
          });
        }
        this.labeledDatasets[label].samples.push(predictedDataSample)
      })
    })
    console.log('Finished parsing labeledDatasets', this.labeledDatasets, Object.keys(this.labeledDatasets))
  }
}
</script>
<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0
}

.label-name:hover {
  @apply bg-gray-200;
}

.label-name.selected {
  @apply font-bold;
  @apply bg-gray-200;
}
</style>
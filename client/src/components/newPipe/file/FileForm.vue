<template>
  <div>
    <b-form-file required
                 v-model="form_.file"
                 :state="Boolean(form_.file)"
                 :placeholder="(this.form_.hasOwnProperty('file') && this.form_.file != null) ? this.form_.file.name : 'Choose/Drop a file...'"
                 browse-text=""
                 class=""
                 @change="fileChanged"
    ></b-form-file>

    <!--TXT FILE-->
    <div
        v-if="Object.prototype.hasOwnProperty.call(this.form, 'file') && this.form_.file != null && this.form_.file.name.endsWith('.txt')"></div>

    <!--CSV FILE-->
    <div
        v-if="Object.prototype.hasOwnProperty.call(this.form,'file') && this.form_.file != null && this.form_.file.name.endsWith('.csv')">
      <b-input-group prepend="Separator" class="" @change="updateCsvSeparator">
        <b-input v-model="form_.csv_separator"></b-input>
      </b-input-group>
      <b-input-group prepend="Column" class="">
        <b-form-select
            class="m-0"
            v-model="form_.csv_column"
            :options="csvColumns"
            required
        ></b-form-select>

      </b-input-group>
    </div>

    <hr/>

    <b-form-checkbox
        v-model="form_.split_on_punctuation"
        class="my-2"
    >Split on Punctuation</b-form-checkbox>

  </div>
</template>

<script>
export default {
  name: 'FileForm',
  props: {
    form: {
      type: Object,
      default() {
        return {
          file: null,
          file_type: null,
          split_on_punctuation: false,
        };
      },
    },
  },
  methods: {
    fileChanged(event) {
      console.log('file changed with event', event)
      let fileNameSplit = this.form_.file.name.split('.');
      this.form_ = {
        file: event.target.files[0],
        file_type: fileNameSplit[fileNameSplit.length-1]
      }
      let config = this.form_;
      this.$emit('file-change', config);
    },
    updateCsvSeparator() {
      const reader = new FileReader();
      const that = this;
      reader.addEventListener('load', (event) => {
        that.csvColumns = event.target.result.split('\n')
            .shift()
            .split(that.form_.csv_separator);
      });
      reader.readAsText(this.form_.file);
    },
  },
  watch: {
    form_: {
      handler: function (event) {
        // console.log('before modification form_ looks like', this.form_);
        console.log('FileForm is handling event', event);
        this.form_ = event;

        // Setting the file extension
        if (Object.prototype.hasOwnProperty.call(this.form_, 'file') && this.form_.file != null) {
          const fileNameSplitted = this.form_.file.name.split('.');
          this.form_.file_type = fileNameSplitted[fileNameSplitted.length - 1];

          // For CSV, looking for columns
          if (this.form_.file.name.endsWith('.csv')) {

            this.form_.csv_separator = ',';
            const reader = new FileReader();
            const that = this;
            reader.addEventListener('load', (event) => {
              that.csvColumns = event.target.result.split('\n')
                  .shift()
                  .split(that.form_.csv_separator);
            });
            reader.readAsText(this.form_.file);
          } else {
            delete this.form_.csv_separator;
            delete this.form_.csv_column;
          }
        }

        let config = this.form_;
        config.file = this.form_.file;
        this.$emit('file-change', config);
      },
      deep: true,
    },
  },
  data() {
    return {
      csvColumns: [],
      form_: {},
    };
  },
  mounted() {
    console.log('setting this.form_ to this.form', this.form_, this.form);
    this.form_ = this.form;
    console.log('now is', this.form_);
  },
};
</script>

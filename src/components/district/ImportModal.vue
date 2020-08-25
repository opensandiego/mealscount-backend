<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div
        class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <header class="modal-header" id="modalTitle">
          <slot name="header">
            <strong>Import from File</strong>

            <button type="button" class="btn-close" @click="close" aria-label="Close modal">x</button>
          </slot>
        </header>
        <section class="modal-body" id="modalDescription">
          <slot name="body">
            <h3>Import from File</h3>
            <div class="filedrop" v-cloak @drop.prevent="addFile" @dragover.prevent>
                Drag File over to import
                <ul>
                    <li v-for="file in files" v-bind:key="file.name">
                        {{ file.name }} ({{ Math.floor(file.size/1024)  }} kb) <button @click="removeFile(file)" title="Remove">X</button>
                    </li>
                </ul>
            </div> 
          </slot>
          <p>
            Accepted formats: .CSV, .XLS, .XLSX. For XLS/XLSX Workbooks, only the first Sheet will be used.
          </p>
          <p>
            <strong>Required Columns:</strong>
            <span v-for="c in required_cols" v-bind:key="c">"{{ c }}" </span>
          </p>
          <p v-if="showComplete" class="col-sm alert alert-success">Import Complete!</p>
        </section>
        <footer class="modal-footer">
          <slot name="footer">
            <button
              type="button"
              class="btn-green"
              @click="do_import"
              aria-label="Do Import"
            >Import</button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
//import Papa from "papaparse";  // no longer needed, XLSX does this and more!
import XLSX from "xlsx";

const REQUIRED_COLS = [
  "school_name",
  "total_enrolled",
  "total_eligible",
  "daily_breakfast_served",
  "daily_lunch_served",
]

export default {
  props: ["district","grouping_index"],
  data() {
    return {
      showComplete: false,
      files: [],
      required_cols: REQUIRED_COLS,
    };
  },
  mounted() {
    this.download_filename =
      "mealscount-district-" + this.district.code + ".csv";
  },
  computed: {
    columns() {
      return [
        "school_code",
        "school_name",
        "total_enrolled",
        "total_eligible",
        "daily_breakfast_served",
        "daily_lunch_served",
        "included_in_optimization",
      ]
    }
  },
  methods: {
    close() {
      this.$emit("close");
    },
    addFile(e){
        // Drag drop from https://www.raymondcamden.com/2019/08/08/drag-and-drop-file-upload-in-vuejs
        const droppedFiles = e.dataTransfer.files;
        if(!droppedFiles) return;
        // this tip, convert FileList to array, credit: https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
        ([...droppedFiles]).forEach(f => {
          this.files.push(f);
        });
    },
    removeFile(file){
      this.files = this.files.filter(f => {
        return f != file;
      });      
    },
    validate_cols(row){
      var missing = [];
      REQUIRED_COLS.forEach( c => {
        if( row[c] == undefined){
          missing.push(c);
        }
      })
      return missing
    },
    parse_rows(rows,district){
      console.log("processing ",rows)
      const missing = this.validate_cols(rows[0]);
      if( missing.length > 0){
        alert("Missing Columns: " + missing.join(",") )
        return
      }
      try{
            if( rows[0].free_lunch_rate != undefined){
              district.rates.free_lunch = Number(rows[0].free_lunch_rate);
              district.rates.paid_lunch = Number(rows[0].paid_lunch_rate);
              district.rates.free_bfast = Number(rows[0].free_bkfst_rate);
              district.rates.paid_bfast = Number(rows[0].paid_bkfst_rate);
            }
            district.schools = [];
            rows.forEach( row => {
                if( row["total_enrolled"] == undefined ){ return; }
                if( row["included_in_optimization"] != undefined){
                  row.active = row.included_in_optimization;
                }else{ row.active = true; }
                row.grouping = null;
                if( row.school_code == null || row.school_code == ""){
                  row.school_code = "school-"+(district.schools.length+1)
                }
                if(row.total_enrolled && row.school_name){
                  district.schools.push( row );
                }
            })
            self.showComplete = true
          }catch(error){
            alert(error.message);
          }
    },
    parse_csv(f,district){
      var self = this;
      Papa.parse(f, {
          header: true,
        complete: function(results) {
          console.log(results.data);
          self.parse_rows(results.data,district);
        }
      });
    },
    parse_xls(f,district){
      var reader = new FileReader();
      var self = this;
      reader.onload = function(e){
        var data = new Uint8Array(e.target.result);
        var workbook = XLSX.read(data, {type: 'array'});
        console.log(workbook);
        const rows = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]]);
        self.parse_rows(rows,district);
      }
      reader.readAsArrayBuffer(f)
    },
    do_import(){
      var district = this.district;
      this.files.forEach( f=> {
        this.parse_xls(f,district);
      })
    }
  }
};
</script>

<style scoped>
input {
  width: 100%;
}
.filedrop {
    margin-top: 10px;
    padding: 10px;
    background-color: #aaa;
    border: solid 1px black;
    min-height: 100px;
}
.filedrop li {
    list-style: none;
}

</style>
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
            <strong>Import from CSV</strong>

            <button type="button" class="btn-close" @click="close" aria-label="Close modal">x</button>
          </slot>
        </header>
        <section class="modal-body" id="modalDescription">
          <slot name="body">
            <h3>Import from CSV</h3>
            <div class="filedrop" v-cloak @drop.prevent="addFile" @dragover.prevent>
                Drag CSV File over to import
                <ul>
                    <li v-for="file in files" v-bind:key="file.name">
                        {{ file.name }} ({{ Math.floor(file.size/1024)  }} kb) <button @click="removeFile(file)" title="Remove">X</button>
                    </li>
                </ul>
            </div> 
          </slot>
          <p>File structure should be exactly the same as the export file. Grouping and Est. Reimbursement will be recalculated.</p>
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
import Papa from "papaparse";

export default {
  props: ["district","grouping_index"],
  data() {
    return {
      showComplete: false,
      files: []
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
    do_import(){
      var district = this.district;
      var self = this;
      this.files.forEach( f=> {
            Papa.parse(f, {
                header: true,
        	    complete: function(results) {
                    console.log(results.data);
                    try{
                      if( results.data[0].free_lunch_rate != undefined){
                        district.rates.free_lunch = Number(results.data[0].free_lunch_rate);
                        district.rates.paid_lunch = Number(results.data[0].paid_lunch_rate);
                        district.rates.free_bfast = Number(results.data[0].free_bkfst_rate);
                        district.rates.paid_bfast = Number(results.data[0].paid_bkfst_rate);
                      }
                      district.schools = [];
                      results.data.forEach( row => {
                          if( row["total_enrolled"] == undefined ){ return; }
                          row.active = row.included_in_optimization.toLowerCase() != 'false' && row.included_in_optimization != '' && row.included_in_optimization != 0;
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
          	    }
            });
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
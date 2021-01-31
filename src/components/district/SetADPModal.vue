<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <header
          class="modal-header"
          id="modalTitle"
        >
          <slot name="header">
            <strong>Set Average Daily Participation</strong>

            <button
              type="button"
              class="btn-close"
              @click="close"
              aria-label="Close modal"
            >
              x
            </button>
          </slot>
        </header>
        <section
          class="modal-body"
          id="modalDescription"
        >
          <slot name="body">
                 <p>Set your ADP for Breakfast and Lunch as a percentage of Total Enrolled.</p>
                 <p><strong>NOTE</strong> This will overwrite any values you have entered. To abort, close this modal.</p>

                 <div class="col mb-3">
                     <label for="breakfast_adp">Breakfast Average Daily Participation:</label><br>
                     <input v-model="breakfast_adp" name="breakfast_adp" type="number" min="0" max="100" />% of Total Enrolled<br>
                 </div>
                 <div class="col mb-3">
                     <label for="lunch_adp">Lunch Average Daily Participation: </label><br>
                     <input v-model="lunch_adp" name="lunch_adp" type="number" min="0" max="100" />% of Total Enrolled<br>
                 </div>
                 <div class="col text-right">
                    <button
                      type="button"
                      class="btn-green"
                      @click="apply"
                      aria-label="Apply"
                    >
                      Apply
                    </button>
                    <button
                      type="button"
                      class="btn-green"
                      @click="close"
                      aria-label="Close modal"
                    >
                        Cancel 
                    </button>
                </div>
           </slot>
        </section>
      </div>
    </div>
  </transition>
</template>

<script>
  export default {
    name: 'modal',
    props: ['breakfast_adp','lunch_adp'],
    methods: {
      close() {
        this.$emit('close');
      },
      apply() {                     
        this.$emit('apply',{breakfast:this.breakfast_adp,lunch:this.lunch_adp})
      },
    },
  };
</script>

<style>
/* TODO drive modal from built-in bootstrap class styles, not explicit unscoped styles */
  .modal-backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background: #FFFFFF;
    box-shadow: 2px 2px 20px 1px;
    padding: 7px;
    overflow-x: auto;
    position: relative;
    display: flex;
    position: relative;
    flex-direction: column;
    align-self: center;
    justify-self: center;
     width: 400px;
    height: 500px;
    margin: 0 auto;
  }

  .modal-header,
  .modal-footer {
    padding: 10x;
    display: flex;
  }

  .modal-header {
    border-bottom: 1px solid #eeeeee;
    color: #4AAE9B;
    justify-content: space-between;
    height: 50px;
    font-weight: 500;
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    justify-content: flex-end;
  }

  .modal-body {
    position: relative;
    padding: 20px 10px;
    /*height: 50px;  */
  }

  .btn-close {
    border: none;
    font-size: 20px;
   
    cursor: pointer;
    font-weight: bold;
    color: #4AAE9B;
    background: transparent;
  }

  .btn-green {
    color: white;
    background: #4AAE9B;
    border: 1px solid #4AAE9B;
    border-radius: 2px;
  }

</style>
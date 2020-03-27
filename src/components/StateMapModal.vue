
<template>
  <transition name="modal-fade">
    <div class="modal-backdrop" v-if="selected_state != null">
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
            <strong>We are sorry! </strong>

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
                 <p>Sorry, {{ selected_state.name }}'s data is not yet available! You can add your district's data and optimize it in our district tool:</p>
                 
                 <p><router-link :to="{name:'district-detail-new',params:{ state_code: selected_state.abbr }}" class="btn btn-green">Enter Your District Data</router-link></p>

                 <p>If you need assistance, we recommend reaching out to your local food policy advocates.</p>
                 <p>If you are interested in helping get data for your state, please contact <a href="https://opensandiego.org">Open San Diego</a></p>
          </slot>
        </section>
        <footer class="modal-footer">
          <slot name="footer">
            

            <button
              type="button"
              class="btn-green"
              @click="close"
              aria-label="Close modal"
            >
              Close me!
            </button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
  export default {
    props: ['selected_state'],
    name: 'modal',
    methods: {
      close() {
        this.$emit('close');
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
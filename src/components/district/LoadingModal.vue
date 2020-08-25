<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div
        class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <section class="modal-body" id="modalDescription">
          <slot name="body">
            <h3>Please Wait</h3>
            <p>Grouping optimizations are currently being run. The results will update shortly.</p>

            <p class="alert alert-info">
                <strong>⚠️ NOTE</strong> We have updated our optimization to run a longer optimization 
                for larger districts directly on the website. This will return better results, but 
                can take up to a few minutes. Please be patient and remain on this page.
            </p>

            <p>
              Elapsed Time: {{ String(Math.floor(elapsed/60)).padStart(2,'0') }}:{{ String(elapsed%60).padStart(2,'0') }}
            </p>
          </slot>
        </section>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  data() {
    return {
      elapsed: 0,
      interval: null,
    };
  },
  mounted() {
    this.elapsed = 0;
    this.interval = setInterval( t => {
      this.elapsed += 1;
    },1000)
  },
  destroyed(){
    clearInterval(this.interval);
    this.interval = null;
  }
}
</script>
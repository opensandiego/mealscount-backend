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
          </slot>
        </section>
      </div>
    </div>
  </transition>
</template>
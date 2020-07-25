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
          </slot>
        </section>
      </div>
    </div>
  </transition>
</template>
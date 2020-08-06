<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div
        class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <header class="modal-header">
          <slot name="header">
            <strong>Welcome to Meals Count District Editing</strong>

            <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close modal">x</button>
          </slot>
        </header>
        <section class="modal-body">
          <slot name="body">
              <h3>Getting Started</h3> <p>You made it to the place where you input your district's schools and school data, and let Meals Count provide recommendations on how to group your schools for your CEP Application.</p>
              <p v-if="district.code == 'new'">We don't have existing school data for this State, so you will need to enter in each school. To start, click "edit" and begin adding your schools in.</p>
              <p v-else>We have prefilled the school data for your District from our data sources, <em>but this is not current and up to date</em>. To edit and adjust the schools and data, begin by pressing "edit"</p>
              <p>If you have any questions, please don't hesitate to <router-link to="/contact">Contact Us!</router-link></p>
          </slot>
        </section>
        <footer class="modal-footer">
          <slot name="footer">
            <button
              type="button"
              class="btn-green"
              @click="$emit('close')"
              aria-label="Close modal"
            >Close me!</button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
    props: ['district'],
}
</script>
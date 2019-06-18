<template lang="pug">
  #cropper-widget 
    img(v-if="cropperImg != 'http://images.kethoughts.com/'" :src="cropperImg" ref="img")
    img(v-else ref="img")

</template>

<script>
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';

export default {
  name: 'cropperWidget',
  props: [
    'cropperImg',
  ],

  data() {
      return {
        cropper: null,
      }
  },

  mounted() {
    const cropper = new Cropper(this.$refs.img, {
      aspectRatio: 1 / 1,
  
    });

    this.cropper = cropper;
  },

  methods: {
      // cropperjs api wrapper
      replace(file) {
        return this.cropper.replace(file)
      },

      getCroppedCanvas() {
        return this.cropper.getCroppedCanvas()
      },

      rotate(degree) {
        // guess what this does :)
        return this.cropper.rotate(degree);
      },
  },

  
}
</script>

<style lang="scss" scoped>

#cropper-widget {
  width: 100%;
  height: 500px;
  border: dashed #cacaca 1px;
  text-align: center;
}

</style>




<template lang="pug">
  #slug-widget 
    .icon-wrapper.wrapper
      i.fa.fa-link
    .url-wrapper.wrapper
      span.root-url {{ url }}
      span.subdirectory-url /{{ subdirectory }}/
      span.slug(v-show="slug && !isEditing") {{ slug }}
      input.input.is-small(type="text" name="slug-edit" v-show="isEditing" v-model="customSlug")
    .button-wrapper.wrapper
      button.button.is-small(v-show="!isEditing" @click.prevent="editSlug") Edit
      button.button.is-small(v-show="isEditing" @click.prevent="saveSlug") Save
      button.button.is-small(v-show="isEditing" @click.prevent="resetSlug") Reset

</template>

<script>
import _ from "lodash";

export default {
 props: {
   url: {
     type: String,
     required: true
   },
   subdirectory: {
     type: String,
     required: true
   },
   title: {
     type: String,
     required:true,
   },
   slugDefault: {
     type: String,
     default: ''
   }
 },
 data() {
    return {
      slug: '',
      isEditing: false,
      customSlug:'',
      wasEdited: false,
      wasChecked: false
    }
  },
  methods: {
    editSlug() {
      this.customSlug = this.slug;
      this.isEditing = true;
    },
    saveSlug() {
      if (this.customSlug != this.slug) this.wasEdited = true;
      this.isEditing = false;
      this.slug = Slug(this.customSlug);
    },
    resetSlug() {
      this.slug = Slug(this.title);
      this.wasEdited = false;
      this.isEditing = false;
    }
  },
  watch: {
    title:_.debounce(function() {
      if(this.wasEdited === false) {
        this.slug = Slug(this.title); // initially generate slug

        // compared with propped slugDefault
        if (this.slugDefault && !this.wasChecked) {
          if (this.slug != this.slugDefault) { this.slug = this.slugDefault; this.wasEdited = true;}
          this.wasChecked = true;
        }
      }
    }, 250),
    slug(val) {
      this.$emit('slug-changed', val);
    }
  }
  
}
</script>

<style scoped>
#slug-widget {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.wrapper {
  margin-left: 8px;
}

.slug {
  background-color: #fdfd96;
  margin: 3px 5px;
}

.wrapper .input {
  width: auto;
}

.url-wrapper {
  height: 30px;
  display: flex;
  align-items: center;
}

.button {
  margin-left: 5px;
}
</style>




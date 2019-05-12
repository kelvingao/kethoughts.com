<template lang='pug'>
  #editWidget
    .columns.m-b-0
    form(v-if="!submitted" @submit="onPublish", method="post", role="form")
        .columns
          .column.is-three-quarters
            b-field
              b-input(type='text', size='is-normal', v-model='post.title')
            slug-widget(url=process.env.VUE_APP_BASE_URI subdirectory='posts' :slugDefault='post.slug' :title='post.title' @slug-changed='updateSlug')
            b-field.m-t-10
              quill-editor(v-model='post.content' ref="QuillEditor"  :options='editorOption')

          .column.is-one-quarter
            .card.card-widget
              .author-widget.widget-area
                .selected-author
                  img(src="https://placehold.it/50x50")
                  .author
                    h4 Kelvin Gao
                    p.subtitle (kelvingao)
              .post-status-widget.widget-area
                .status
                  .status-icon
                    b-icon(icon="file-alt" size="is-large")
                  .status-details
                    h4 #[span.status-emphasis Draft] Saved
                    p A Few Minutes Ago 
              .publish-buttons-widget.widget-area
                .secondary-action-button
                  button.button.is-info.is-outlined.is-fullwidth Save Draft
                .primary-action-button
                  button.button.is-primary.is-fullwidth Publish
            
            .image-url-widget.m-t-10
              h2 featured image: {{ post.featured_image }}
              input(type="file" @change="onFileChanged" ref="imageInput")
              button(type="button" @click="onUpload") Upload
    div(v-else) Thanks for adding your post!

</template>
<script>
import api from '@/api';
import slugWidget from '@/components/widgets/slugWidget';
import hljs from 'highlight.js'
const STATICDOMAIN = 'http://images.kethoughts.com'

export default {
  props: {
   post: {},
  },
  name: 'EditWidget',
  components: {
    slugWidget,
  },
  data() {
    return {
      submitted: false,
      selectedFile: null,
      editorOption: {
        modules: {
          toolbar: [
            ['bold', 'italic', 'underline', 'strike'],
            ['blockquote', 'code-block'],
            [{ 'header': 1 }, { 'header': 2 }],
            [{ 'list': 'ordered' }, { 'list': 'bullet' }],
            [{ 'script': 'sub' }, { 'script': 'super' }],
            [{ 'indent': '-1' }, { 'indent': '+1' }],
            [{ 'direction': 'rtl' }],
            [{ 'size': ['small', false, 'large', 'huge'] }],
            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
            [{ 'font': [] }],
            [{ 'color': [] }, { 'background': [] }],
            [{ 'align': [] }],
            ['clean'],
            ['link', 'image', 'video']
          ],
          syntax: {
            highlight: text => hljs.highlightAuto(text).value
          }
        }
      },
    }
  },

  mounted() {
    this.$refs.QuillEditor.quill.getModule('toolbar').addHandler('image', this.quillImageHandler)
  },

  methods: {
    onFileChanged (event) {
      this.selectedFile = event.target.files[0]
    },
    onUpload() {
      api.saveImageToQiniu('kelvin', this.selectedFile).then( res => {
        this.post.featured_image = res.key
      });
    },

    onPublish(evt) {
      evt.preventDefault();

      /* create or edit a post */
      api.editPost(this.post)
        .then(resp => {
          this.submitted = true;
          this.$router.go(-1)
        })
        .catch(err => {
          console.error(err)
        })
    },

    updateSlug(val) {
      this.post.slug = val;
    },

    quillImageHandler() {
      const input = document.createElement('input');
      input.setAttribute('type', 'file');
      input.click();
      // Listen upload local image and save to server
      input.onchange = () => {
        const file = input.files[0];
        // File type is only image.
        if (/^image\//.test(file.type)) {
          api.saveImageToQiniu('kelvin', file).then( (res) => {
            this.insertToEditor(res.key)
          });
        } else {
          console.warn('You could only upload images.');
        }
      }
    },

    insertToEditor(key) {
      // Push image url to rich editor.
      const range = this.$refs.QuillEditor.quill.getSelection();
      this.$refs.QuillEditor.quill.insertEmbed(range.index, 'image', STATICDOMAIN + '/' + key);
    }

    
  },
}
</script>

<style lang="scss" scoped>

/deep/ .ql-editor {
  height:760px;
  background: white;
}

.quill-code {
  border: none;
  height: auto;

  > code {
    width: 100%;
    margin: 0;
    padding: 1rem;
    border: 1px solid #ccc;
    border-top: none;
    border-radius: 0;
    height: 10rem;
    overflow-y: auto;
    resize: vertical;
  }
}

/* make title border same as ql-editor */
/deep/ input[type=text] {
  border: 1px solid #ccc;
  border-radius: 0;
}

@media screen and (min-width: 1087px) {
  .columns > .column:first-child {
    padding-right: 0;
  }
}
</style>

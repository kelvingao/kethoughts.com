<template lang='pug'>
  #editWidget
    .columns.m-b-0
    form(@submit="onPublish", method="post", role="form")
        .columns
          .column.is-three-quarters
            b-field
              b-input(type='text', size='is-normal', v-model='post.title')
            slug-widget(url=process.env.VUE_APP_BASE_URI subdirectory='posts' :slugDefault='post.slug' :title='post.title' @slug-changed='updateSlug')
            b-field.m-t-10
              quill-editor(v-model='post.content' ref="QuillEditor"  :options='editorOption')

          .column.is-one-quarter
            //- PUBLISH WIDGET
            .card.publish-widget
              header.card-header
                p.card-header-title Publish
                a(aria-label="more options" @click="showPublish = !showPublish").card-header-icon
                  b-icon(v-if="showPublish" icon="angle-down" size="is-small")
                  b-icon(v-else icon="angle-up" size="is-small")
              
              #publish-sections(v-show="showPublish")
                //- SECTION 1: draft and priview buttons
                .draft-preview-section.section-area
                  .draft-button
                    button.button.is-light #[strong Save Draft]
                  .preview-button
                    button.button.is-light.is-pulled-right #[strong Preview]

                //- SECTION 2: status, visibility and scheduled section
                .status-section.section-area
                  //- STATUS
                  .status-display.m-b-5
                    b-icon(icon="bookmark" custom-size="null").m-r-5
                    | Status:
                    span.m-l-5 #[strong {{ post.status | postStatusDisplay }}]
                    a(v-show="!editingStatus && post.status != 'private' " @click="editingStatus=true").m-l-5(style="text-decoration: underline; ") Edit
                    //- status editing
                    #status-editing(v-if="editingStatus").m-l-5.p-5
                      b-field
                        b-select(v-model="selectedOption" size="is-small")
                          option(value="publish") Public
                          option(value="private") Private
                        a.m-l-5.button.is-small.is-primary OK
                        a.m-l-5(@click="editingStatus=false" style="text-decoration: underline;") Cancel

                  //- VISIBILITY
                  .visibility-display.m-b-5
                    b-icon(icon="eye" custom-size="null").m-r-5
                    | Visibility:
                    span.m-l-5 #[strong {{ post.status | postVisibilityDisplay }}]
                    a(v-show="!editingVisibility" @click="editingVisibility=true").m-l-5(style="text-decoration: underline; ") Edit
                    //- visibility editing
                    #visibility-selection(v-if="editingVisibility")
                      .m-l-10.m-b-5
                        b-radio(v-model="radioVisibilitySelection" native-value="publish" size="is-small") Public
                        br
                        b-radio(v-model="radioVisibilitySelection" native-value="password" size="is-small") Protected
                        br
                        b-radio(v-model="radioVisibilitySelection" native-value="private" size="is-small") Private
                        br
                      a.m-l-5(@click="onVisibilityChanged").save-post-status.button.is-small.is-primary OK
                      a.m-l-5(@click="editingVisibility=false" style="text-decoration: underline;") Cancel

                  //- SCHEDULE
                  .schedule-display.m-b-5
                    b-icon(icon="calendar-alt" custom-size="null").m-r-5
                    | Publish:
                    span.m-l-5 #[strong Immediately]
                    a(v-show="!editingStatus" @click.prevent="editingStatus=true").m-l-5(style="text-decoration: underline; ") Edit

                //- SECTION 3: publish footer
                .publish-footer-section.section-area
                  .move-to-trash
                    a(style="text-decoration: underline;") Move To Trash
                  .publish-button
                    input(type="submit" value="Publish" style="font-weight: bold").button.is-primary.is-pulled-right
           
            //- TAGS WIDGET
            .card.m-t-10
              header.card-header
                p.card-header-title Tags
                a(aria-label="more options" @click="showTags = !showTags").card-header-icon
                  b-icon(v-if="showTags" icon="angle-down" size="is-small")
                  b-icon(v-else icon="angle-up" size="is-small")

              //- SECTION: tags
              .tags-section.section-area(v-show="showTags")
                .tags-section-list(v-if="!isEditTags")
                  b-taglist
                    b-tag(v-for="tag in post.tags" type="is-dark" closable @close="remove(tag)") {{ tag }} 
                    a(@click='isEditTags = true' style="text-decoration: underline; margin-bottom: 0.5rem;") Mange Tags
                .tags-section-edit(v-else)
                  b-field
                    b-taginput.m-r-5(v-model="post.tags" v-show="isEditTags" attached size="is-normal" ellipsis expanded)
                    button(@click.prevent="isEditTags=false" size="is-normal").button.is-primary #[strong Done]
            
            //- FEATURED IMAGE WIDGET
            .card.m-t-10
              header.card-header.m-t-10
                p.card-header-title Featured Image
                a(aria-label="more options" @click="showFeatured = !showFeatured").card-header-icon
                  b-icon(v-if="showFeatured" icon="angle-down" size="is-small")
                  b-icon(v-else icon="angle-up" size="is-small")
              
              .featured-image-sections(v-show="showFeatured")
                //- SECTION 1: image display
                .image-section.section-area
                  .card-image(v-if="post.featured_image != ''").p-10
                    figure.image
                      img(:src='staticdomain + "/" + post.featured_image')

                //- SECTION 2: image selection & upload
                .image-upload-section.section-area
                  .image-select-button
                    b-upload(type="file" v-model="selectedFile" ref="imageInput")
                      .button.is-light(style="background: whitesmoke")
                        b-icon(icon="upload")
                        span #[strong Select Image]
                  .selected-file-name(v-if="selectedFile").p-l-5 {{ selectedFile.name }}
                  .image-upload-button(v-if="selectedFile")
                    button(@click.prevent="onUpload(selectedFile)").button.is-primary.is-pulled-right #[strong Upload]
</template>
<script>
import api from '@/api';
import slugWidget from '@/components/widgets/slugWidget';
import hljs from 'highlight.js'

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
      staticdomain: 'http://images.kethoughts.com',
      selectedOption: 'publish',
      showPublish: true,
      showTags: true,
      showFeatured: true,
      editingStatus: false,
      editingVisibility: false,
      radioVisibilitySelection: this.post.status, // FIXME: this widget has been created along with parent component, issue 'undefined'.
      isEditTags: false,
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
    onVisibilityChanged() {
      this.post.status = this.radioVisibilitySelection
      this.editingVisibility = false
    },

    remove(tag) {
      for (let i = 0; i < this.post.tags.length; i++) {
        if (this.post.tags[i] === tag) {
          this.post.tags.splice(i, 1);
          break;  //<-- Uncomment  if only the first term has to be removed
        }
      }
    },
  
    onUpload(file) {
      api.saveImageToQiniu('kelvin', file).then( res => {
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
      this.$refs.QuillEditor.quill.insertEmbed(range.index, 'image', this.staticdomain + '/' + key);
    }

  },

  filters: {
    postVisibilityDisplay(status) {
      let display = "Public"

      switch(status) {
        case 'private':
          display = 'Private'
          break
        case 'password':
          display = 'Protected'
          break
      }

      return display
    },

    postStatusDisplay(status) {
      let display = 'Published'

      switch(status) {
        case 'private':
          display = 'Privately Published'
          break
        case 'future':
          display = 'Scheduled'
          break
        case 'pending':
          display = 'Pending Review'
          break
        case 'draft':
        case 'auto-draft':
          display = 'Draft'
          break
      }
      return display
    }
  }

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

.section-area {
  align-items: center;

  /* PUBLISH WIDGET */
  &.draft-preview-section {
    display: flex;
    padding: 10px 10px 0 10px;

    .draft-button, .preview-button {
      flex: 1;
      margin: 0 5px;
    }
  }

  &.status-section {
    padding: 10px;
  }

  &.publish-footer-section {
    background: whitesmoke;
    display: flex;
    padding: 10px;
    .move-to-trash, .publish-button {
      flex: 1;
      margin: 0 5px;
    }
  }

  /* TAGS WIDGET */
  &.tags-section {
    display: flex;
    padding: 10px;
    min-height: 60px;

    .tags-section-list, .tags-section-edit {
      flex: 1;
      margin: 0 5px;
    }
  }

  /* FEATURED IMAGE WIDGET */
  &.image-upload-section {
    display: flex;
    align-items: center;
    padding: 10px;

    .image-upload-button, .image-select-button, {
      flex: 1;
    }

    .selected-file-name {
      width:100%;
      overflow:hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }
}

@media screen and (min-width: 1087px) {
  .columns > .column:first-child {
    padding-right: 0;
  }
}
</style>

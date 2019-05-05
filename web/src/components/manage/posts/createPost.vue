<template lang='pug'>
  #createPost
    .flex-container
      .columns.m-b-0
      form(v-if="!submitted" @submit="onSubmit", method="post", role="form")
          .columns
            .column.is-three-quarters
              b-field
                b-input(type='text', size='is-normal', v-model='post.title')
              slug-widget(url=process.env.VUE_APP_BASE_URI subdirectory='posts' :title='post.title' @slug-changed='updateSlug')
              b-field.m-t-10
                quill-editor(v-model='post.content', :options='editorOption')

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
      div(v-else) Thanks for adding your post!

</template>
<script>
import api from '@/api';
import slugWidget from '@/components/widgets/slugWidget';
import hljs from 'highlight.js'

export default {
  name: 'CreatePost',
  components: {
    slugWidget,
  },
  data() {
    return {
      submitted: false,
      post: {
        title:'',
        slug:'',
        content:'',
        excerpt: ''
      },
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
      }
    }
  },

  methods: {
    onSubmit(evt) {
      evt.preventDefault();

      const { title, slug, content, excerpt } = this.post;
      api.createPost({title, slug, content, excerpt})
        .then(resp => {
          this.submitted = true;
          this.$router.go(-1)
        })
        .catch(err => {
          console.log(err)
        })
    },
    updateSlug(val) {
      this.post.slug = val;
    },
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

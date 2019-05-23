import axios from "axios";
import * as qiniu from 'qiniu-js'

export default {

/*--------------------------------------------------------------
Posts REST APIs
--------------------------------------------------------------*/

/**
 * Edit or create (if post.id is null) a post.
 *
 * @param  { Object }  post - id, title, content, slug, excerpt
 * @return { Promise }
 */
editPost(post) {
  // must authenticated
  axios.defaults.headers.common['Authorization'] = localStorage.getItem('Authorization')

  return new Promise((resolve, reject) => {
    axios.post(process.env.VUE_APP_BASE_URI + "/api/posts", post)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
    })
},

/**
 * Delete a post.
 *
 * @return { Promise }
 */
deletePost(id) {
  // must authenticated
  axios.defaults.headers.common['Authorization'] = localStorage.getItem('Authorization')

  return new Promise((resolve, reject) => {
    axios.delete(process.env.VUE_APP_BASE_URI + "/api/posts?id=" + id)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},

/**
 * Get all posts.
 *
 * @return { Promise }
 */
getPosts(visibility = 'publish') {
  return new Promise((resolve, reject) => {
    axios.get(process.env.VUE_APP_BASE_URI + "/api/posts?visibility=" + visibility)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},

/**
 * Get a post by slug.
 *
 * @param  { Object }  slug - post slug
 * @return { Promise }
 */
getPostBySlug(slug) {
  return new Promise((resolve, reject) => {
    axios.get(process.env.VUE_APP_BASE_URI + "/api/posts?slug=" + slug)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},

/**
 * Get a post by id.
 *
 * @param  { Object }  id - post id
 * @return { Promise }
 */
getPostById(id) {
  return new Promise((resolve, reject) => {
    axios.get(process.env.VUE_APP_BASE_URI + "/api/posts?id=" + id)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},


/*--------------------------------------------------------------
Users REST APIs
--------------------------------------------------------------*/

/**
 * Post authentication request, return the token.
 *
 * @param  { Object }  auth - user email, password
 * @return { Promise }
 */
postAuthorization(auth) {
  return new Promise((resolve, reject) => {
    axios.post(process.env.VUE_APP_BASE_URI + "/api/auth/login", auth)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},

/**
 * Get users information.
 *
 * @return { Promise }
 */
getUsers() {
  return new Promise((resolve, reject) => {
    axios.get(process.env.VUE_APP_BASE_URI + "/api/users")
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},


/*--------------------------------------------------------------
Qiniu JS APIs
--------------------------------------------------------------*/

/**
 * Get authenticated token.
 *
 * @param { String } bucket - bucket name
 * @return { Promise }
 */
getQiniuToken(bucket, filename) {
  return new Promise((resolve, reject) => {
    axios.get(process.env.VUE_APP_BASE_URI + "/api/qiniu?bucket=" + bucket + '&filename=' + filename)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},

/**
 * Save image to Qiniu cloud.
 *
 * @param { String } bucket - bucket name
 * @return { Promise }
 */
saveImageToQiniu(bucket, file) {
  const config = {
      useCdnDomain: true,
      region: qiniu.region.z0
  };

  const putExtra = {
      fname: file,
      params: {},
      mimeType: ["image/png", "image/jpeg", "image/gif"]
  };

  const fd = new FormData();
  fd.append('image', file);

  return new Promise((resolve, reject) => {
    /* get token and upload */
    this.getQiniuToken(bucket, file.name).then( res => {
      const token = res.data
      const observer = {
        next(res) {
          console.log('uploading progress: ' + res.total.percent + ' %');
        },
        error (err) {
          reject(err)
        },
        complete (res) {
          resolve(res)
        }
      }
      let observable = qiniu.upload(file, file.name, token, putExtra, config)
      /* Start uploading... */
      observable.subscribe(observer)
    }).catch(err => {
      reject(err)
    })
  })
},


/*--------------------------------------------------------------
Weixin JS API
--------------------------------------------------------------*/

/**
 * Weixin signature request.
 *
 * @param  { String }  url - request url
 * @return { Promise }
 */
getWeixinJsSdk(url) {
  return new Promise((resolve, reject) => {
    axios.post(process.env.VUE_APP_BASE_URI + "/api/weixin/signature", url)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},

}
import axios from "axios";

export default {

/*--------------------------------------------------------------
Post REST APIs
--------------------------------------------------------------*/

/**
 * Create a post.
 *
 * @param  { Object }  post - title, content, slug, excerpt
 * @return { Promise }
 */
createPost(post) {
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
 * Edit a post.
 *
 * @return { Promise }
 */
editPost(id, post) {
  // must authenticated
  axios.defaults.headers.common['Authorization'] = localStorage.getItem('Authorization')

  return new Promise((resolve, reject) => {
    axios.post(process.env.VUE_APP_BASE_URI + "/api/posts?id=" + id, post)
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
getPosts() {
  return new Promise((resolve, reject) => {
    axios.get(process.env.VUE_APP_BASE_URI + "/api/posts")
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
},

/**
 * Get a post by slug,
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
 * Get a post by id,
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
User REST APIs
--------------------------------------------------------------*/

/**
 * Post authentication request, get the token.
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
 * Get all users information.
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

}
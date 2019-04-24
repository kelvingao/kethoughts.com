import axios from "axios";

export default {

/*--------------------------------------------------------------
REST API Requester
--------------------------------------------------------------*/

/**
 * Post authentication request to backend server,
 * if OK, return the token.
 *
 * @param  { Object }  auth - user email & password
 * @return { Promise }
 */
postAuthorization(auth) {
  return new Promise((resolve, reject) => {
    axios.post(process.env.VUE_APP_BASE_URI + "api/auth/login", auth)
      .then(resp => {
        resolve(resp.data)
      }).catch(err => {
        reject(err)
      })
  })
},

/**
 * Get users info request to backend server.
 *
 * @return { Promise }
 */
getUsers() {
  return new Promise((resolve, reject) => {
    axios.get(process.env.VUE_APP_BASE_URI + "api/users")
      .then(resp => {
        resolve(resp.data)
      })
      .catch(err => {
        reject(err)
      })
  })
},

}
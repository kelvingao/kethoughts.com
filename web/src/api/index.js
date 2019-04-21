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
    axios({
      method: 'post',
      url: process.env.VUE_APP_BASE_URI + "api/auth/login",
      data: auth
    }).then(resp => {
      resolve(resp)
    }).catch(err => {
      reject(err)
    })
  })
},

}
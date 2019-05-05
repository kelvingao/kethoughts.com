import api from '@/api'
import jwt_decode from 'jwt-decode'

export default {

/*--------------------------------------------------------------
Authentication Actions
--------------------------------------------------------------*/

/**
 * Post authentication request to backend server,
 * if OK, store the token, via REST API.
 *
 * @param  { Object }  auth - user email & password
 * @return { Promise }
 */
AUTH_REQUEST:({ commit }, auth) => {
  return new Promise((resolve, reject) => {
    commit('AUTH_REQUEST')  // 'loading' state
    api.postAuthorization(auth)
      .then(res => {
        const token = res.data.token
        localStorage.setItem('Authorization', token) // store the token in localstorage
        commit('AUTH_SUCCESS', token)  // 'success' state
        resolve(res)
      })
      .catch(err => {
        commit('AUTH_ERROR', err)   // 'error' state
        localStorage.removeItem('Authorization')  // if the request fails, remove any possible user token
        reject(err)
      })
  })
},

/**
 * Inspect decoded token whether expired,
 * if time is expired, remove vuex and localStorage token.
 *
 */
AUTH_INSPECT_TOKEN: ({ commit, state }) => {
  const token = state.token

  if(token) {
    const decoded = jwt_decode(token);
    const exp = decoded.exp

    if (exp <= (Date.now() / 1000)) {
      commit('AUTH_EXPIRED')
      localStorage.removeItem('Authorization')
    }
  } 
},

/**
 * Log out, remove vuex and localStorage token.
 *
 * @return { Promise }
 */
AUTH_LOGOUT: ({ commit }) => {
  return new Promise((resolve, reject) => {
    commit('AUTH_LOGOUT')
    localStorage.removeItem('Authorization') // clear token from localstorage
    resolve()
  })
},

}
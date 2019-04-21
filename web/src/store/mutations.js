export default {

/*--------------------------------------------------------------
Authentication status
--------------------------------------------------------------*/

AUTH_REQUEST: (state) => {
  state.status = 'loading';
},

AUTH_SUCCESS: (state, token) => {
  state.status = 'success';
  state.token = token;
},

AUTH_ERROR: (state) => {
  state.status = 'error';
},

AUTH_EXPIRED: (state) => {
  state.status = 'expired';
  state.token = '';
},

AUTH_LOGOUT: (state) => {
  state.status = 'logout';
  state.token = '';
},

}
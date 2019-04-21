import jwt_decode from 'jwt-decode'

export default {

isAuthenticated: state => !!state.token,

loggedInUser: (state) => {
    const token = state.token
    const decoded = jwt_decode(token)  // decode jwt token
    return decoded.user
}

}

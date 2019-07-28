console.log('csrf:', csrf)
// sent a daat to back-end
// axios.post('/path',{data}, {setting})
// axios.post('/hello', {
//         name: 'user1'
//     }, {
//         headers: {
//             'x-csrf-token': csrf
//         }
//     })
//     // .then(response=>{})
//     .then(function (response) {
//         console.log('[ data sent success]', response)
//     })
//     .catch(error => {
//         console.log(error)
//     })

// function for log out
function logout() {
    axios.post('/logout', {}, {
            headers: {
                "x-csrf-token": csrf
            }
        })
        .then(response => {
            //console.log("success to sign in")
            console.log(response)
            // go back home
            location = '/'
        })
        .catch(error => {
            //console.log("fail to sign in")
            console.log(error)
        })
}

// function for log in
function login(event) {
    console.log('[ start login ]')
    //cancel that web refresh screen
    event.preventDefault()
    // get user's filled email and passsage
    const email = document.getElementById('loginEmail').value,
        password = document.getElementById('loginPassword').value;
    console.log('[email]', email);
    console.log('[password]', password);
    // firebase login
    firebase.auth().signInWithEmailAndPassword(email, password)
        .then(response => {
            response.user.getIdToken()
                .then(idToken => {
                    // get id token
                    console.log(idToken);
                    // define data which is sent to backend
                    const data = {
                        idToken: idToken
                    }
                    // take id token POST to the rotue
                    axios.post('/login', data, {
                            headers: {
                                "x-csrf-token": csrf
                            }
                        })
                        .then(response => {
                            console.log("success to sign in")
                            console.log(response)
                            location.reload()
                        })
                        .catch(error => {
                            console.log("fail to sign in")
                            console.log(error)
                        })

                })
        })
        .catch(error => {
            console.log(error)
        })

}
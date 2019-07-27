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
            console.log(response)
        })
        .catch(error => {
            console.log(error)
        })

}
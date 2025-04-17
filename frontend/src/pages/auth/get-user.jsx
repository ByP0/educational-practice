export const getUser=async(emailToFind)=>{
    return fetch(`http://127.0.0.1:8000/sing_up?email=${emailToFind}`)
    .then((loadedUser)=>loadedUser.json())
    .then(([loadedUser])=>loadedUser&&{
        first_name: loadedUser.first_name,
        last_name: loadedUser.last_name,
        patronymic: loadedUser.patronymic,
        email: loadedUser.email,
        password: loadedUser.password ,
        birth_date: loadedUser.birth_date
    })
}
export const getForts= async(id)=>{



    const session=localStorage.getItem('session')
    console.log(session);


    const res = await fetch(`http://localhost:8000/forts/?fort_id=${id}`,{
        method:'GET',
        headers:{
            'accept': 'application/json',
            'user-session': session
        }
    })
    return await res.json()
}
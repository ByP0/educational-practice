
export const getUser=async(data)=>{

     const res=await fetch(`http://127.0.0.1:8000/me`,{
        method:"GET",
        headers:{
            'accept': 'application/json',
            'user-session': data
        }
    })
    return await res.json()

    }

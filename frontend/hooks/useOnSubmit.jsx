 import{useNavigate} from 'react-router-dom'


export const useOnSubmit=()=>{

    const navigate= useNavigate()
    

    return async (data)=>{
        try{
            const res = await fetch(`http://127.0.0.1:8000/sign_in`,{
                method:"POST",
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'email': data.email,
                    'password': data.password
                  })
            })
            if(res.status===404){
                alert('Пользователь не найден')
            }
            const userSession = await res.json()
            if(userSession.session) navigate('/')
        }catch(e){
            console.error('Ошибка:', e);
        alert('Ошибка при отправке: ' + e.message);
        }
    }

   
    
  
 }
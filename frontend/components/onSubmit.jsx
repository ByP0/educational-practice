 import{useNavigate} from 'react-router-dom'
 import { getUser } from '../api/get-user'
 import {setUser} from '../action/set-user'
 import { useDispatch } from 'react-redux'


export const OnSubmit=()=>{

    const dispatch = useDispatch()
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
            console.log(userSession.session);
            if(userSession.session){
                localStorage.setItem('session',userSession.session)
                 const userData=await getUser(userSession.session)
                 dispatch(setUser(userData))
                navigate('/')
            }
        }catch(e){
            console.error('Ошибка:', e);
        alert('Ошибка при отправке: ' + e.message);
        }
    }
 }
 
import { Input } from "./componets/Input"
import { Button } from "./componets/Button"
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from 'react-hook-form'
import * as yup from 'yup'
import './auth.css'
;

    const authFormScheme=yup.object().shape({
        email: yup
        .string()
        .email('Введите корректный email')
        .required('Заполните email') 
        .max(50, 'Email не может содержать более 50 символов'),
        password: yup
        .string()
        .required('Заполните пароль')
        .matches(/^[\w#%]+$/,"Неверно заполнен пароль")
        .min(6)
        .max(30)
    })

    export const AuthorizeForm=()=>{


        const {register,handleSubmit,formState:{errors}}=useForm({
            defaultValues:{
                email:'',
                password:''
            },
            resolver:yupResolver(authFormScheme)
        })

         const onSubmit=async(data)=>{
            console.log(data)
            try{
                const res = await fetch(`http://localhost:8000/sing_in`,{
                    method:"POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'email': data.email,
                        'password': data.password
                      })
                })
                
                if (!res.ok) throw new Error('Ошибка сервера');
            }catch(e){
                console.error('Ошибка:', e);
            alert('Ошибка при отправке: ' + e.message);
            }
            
          
         }
        
    return(
        <div className="form">
            <form className="form-auth" onSubmit={handleSubmit(onSubmit)}>
                <h2>Вход</h2>
                <div>
                    <p>Электронная почта</p>
                <Input placeholder='Введите email...'name='email'{...register('email')}/>
                {errors.email&&<div>{errors.email.message}</div>}
                </div>
                <div>
                    <p>Пароль</p>
                <Input placeholder='Введите пароль...'name='password'{...register('password')}/>
                {errors.password && <div>{errors.password.message}</div>}
                </div>
                <Button type="submit">Войти</Button>  
            </form>
        </div>
    )
}
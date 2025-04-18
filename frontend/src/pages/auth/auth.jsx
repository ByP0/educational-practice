import { Input } from "./componets/Input"
import { Button } from "./componets/Button"
import { yupResolver } from "@hookform/resolvers/yup";

import { useForm } from 'react-hook-form'
import { useOnSubmit } from "../../../hooks/useOnSubmit.jsx";
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

        const onSubmit=useOnSubmit()

        
        
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
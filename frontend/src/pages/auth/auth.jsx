import { Input } from "./componets/Input"
import { Button } from "./componets/Button"
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from 'react-hook-form'
import { OnSubmit } from "../../../components/onSubmit.jsx";
import { Link } from "react-router-dom";
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

        const onSubmitUser=OnSubmit()

        
        
    return(
        <div className="form">
            <form className="form-auth" onSubmit={handleSubmit(onSubmitUser)}>
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
                <div className="btn-group">
                <Button type="submit" id="entry">Войти</Button>  
                <Link to="/register" ><Button id="register">Регистрация</Button></Link>
                </div>
            </form>
        </div>
    )
}
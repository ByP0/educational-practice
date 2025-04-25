import { Input } from "../auth/componets/Input"
import { Button } from "../auth/componets/Button"
import { useForm } from "react-hook-form"
import { yupResolver } from "@hookform/resolvers/yup"
import * as yup from 'yup'
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { setUser } from "../../../action/set-user"
import { getUser } from "../../../api/get-user"
import { useState } from "react"
import './register.css'






const registFormScheme=yup.object().shape({
    firstName: yup
    .string()
    .required('Имя обязательно')
    .min(2, 'Имя должно быть не менее 2 символов'),
  lastName: yup
    .string()
    .required('Фамилия обязательна')
    .min(2, 'Фамилия должна быть не менее 2 символов'),
  middleName: yup
    .string()
    .nullable()
    .notRequired(),
    email: yup
    .string()
    .email('Введите корректный email')
    .required('Заполните email') 
    .max(50, 'Email не может содержать более 50 символов'),
  password: yup
    .string()
    .required('Пароль обязателен')
    .min(6, 'Пароль должен быть не менее 6 символов'),
  birthDate: yup
    .string()
    .matches(
        /^\d{4}-\d{2}-\d{2}$/,
        'Дата должна быть в формате ДД-ММ-ГГГГ'
      )
    .typeError('Введите корректную дату')
    .required('Дата рождения обязательна')
    .max(new Date(), 'Дата рождения не может быть в будущем'),
})


export const RegisterForm=()=>{

    const dispatch=useDispatch()
    const navigate=useNavigate()
    const [loading,setLoading]=useState(false)

    const {register,handleSubmit,formState:{errors}}=useForm({
        defaultValues:{
            firstName:'',
            lastName:'',
            middleName:'',
            email:'',
            password:'',
            birthDate:''
        },
        resolver:yupResolver(registFormScheme)
    })

    const onSubmit=async(data)=>{
        setLoading(true)
        const res =await fetch(`http://localhost:8000/sign_up`,{
            method:'POST',
            headers:{
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body:JSON.stringify({
                'first_name': data.firstName,
                'last_name': data.lastName,
                'patronymic': data.middleName,
                'email': data.email,
                'password': data.password,
                'birth_date': data.birthDate
              })
        }).finally(()=>setLoading(false))
        if(res.status===400){
            alert('Пользователь уже заргестрирован')
        }
        const userSession=await res.json()
        if(userSession.session){
            const userData=await getUser(userSession.session)
            dispatch(setUser(userData))
            navigate('/')
        }
        
    }
    if (loading) {
        return (
            <div className="loader-wrapper">
                <div className="spinner"></div>
            </div>
        );
    } 
    return(
        <div>
            <form className="form-register" onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <h2>Регистрация</h2>
                </div>
                <div>
                    <p>Имя</p>
                    <Input {...register('firstName')} />
                    {errors.firstName&&<div>{errors.firstName.message}</div>}
                </div>
                <div>
                    <p>Фамилия</p>
                    <Input {...register('lastName')}/>
                    {errors.lastName&&<div>{errors.lastName.message}</div>}
                </div>
                <div>
                    <p>Отчество</p>
                    <Input {...register('middleName')} />
                    {errors.middleName&&<div>{errors.middleName.message}</div>}
                    </div>
                <div>
                    <p>Почта</p>
                    <Input {...register('email')} name='email' type='email'/>
                    {errors.email&&<div>{errors.email.message}</div>}
                    </div>
                <div>
                    <p>Пароль</p>
                    <Input {...register('password')}name='password' type='password'/>
                    {errors.password&&<div>{errors.password.message}</div>}
                    </div>
                <div>
                    <p>Дата рождения</p>
                    <Input {...register('birthDate')} /></div>
                    {errors.birthDate&&<div>{errors.birthDate.message}</div>}
                    <div>
                        <Button id='regist'>Зарегистрироваться</Button>
                    </div>
            </form>
        </div>
    )
}
import { Input } from "../auth/componets/Input"
import './register.css'

export const Register=()=>{
    return(
        <div>
            <form className="form-register">
                <div>
                    <p>Имя</p>
                    <Input/>
                </div>
                <div>
                    <p>Фамилия</p>
                    <Input/>
                </div>
                <div>
                    <p>Отчество</p>
                    <Input/>
                    </div>
                <div>
                    <p>Пароль</p>
                    <Input/>
                    </div>
                <div>
                    <p>Дата рождения</p>
                    <Input/></div>
            </form>
        </div>
    )
}
import { getUser } from "./get-user"


export const authorize=async(authEmail,authPassword)=>{
    
    const user=await getUser(authEmail)
    

    if(!user){
        return{
            error:"Такой пользователь не найден",
            res:null
        }
    }

    const {password}=user
    if(authPassword!==password){
        return{
            error:'неверный пароль',
            res:null
        }
    }
    return{
        error:null,
        res:{
            

        }
    }
}
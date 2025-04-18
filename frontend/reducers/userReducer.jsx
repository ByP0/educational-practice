import { ACTION_TYPE } from "../action/action-type"

const initialState={
first_name: null,
last_name: null,
patronymic: null,
email: null,
password: null,
birth_date: null
}

export const userReducer=(state=initialState,action)=>{
    switch(action.type){
        case ACTION_TYPE.SET_USER:{
            return{
                ...state,
                ...action.type
            }
        }
        default:
            return state
    }

}
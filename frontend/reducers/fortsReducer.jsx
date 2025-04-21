import { ACTION_TYPE } from "../action/action-type"

const initialState={
    fort_id: null,
    fort_name: null,
    description:null,
    images:[
        {
            
            image_id: null,
            filename: null,
            content_type:null,
            image_data:null
        }
    ]
}

export const fortsReducer=(state=initialState,action)=>{
    switch(action.type){
        case ACTION_TYPE.SET_FORTS:{
            return{
                ...state,
                ...action.payload
            }
        }
        default:
            return state
    }

}
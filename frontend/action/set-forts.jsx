import { ACTION_TYPE } from "./action-type";

export const setForts=(forts)=>({
    type:ACTION_TYPE.SET_FORTS,
    payload:forts
})
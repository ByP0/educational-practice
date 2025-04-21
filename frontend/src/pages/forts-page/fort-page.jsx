import { useParams } from "react-router-dom"
import { getForts } from "../../../api/get-forts"
import { useEffect,useState } from "react"
import { useDispatch } from "react-redux"
import { setForts } from "../../../action/set-forts"
import { useSelector } from "react-redux"
import { seletFortsName } from "../../../selectors/select-forts-name"
import { selectImgForts } from "../../../selectors/select-img-forts"
import { selectDesForts } from "../../../selectors/select-des-forts"
import { Input } from "../auth/componets/Input"
import { Button } from "../auth/componets/Button"
import './forts-page.css'


export const FortsPage=()=>{
    
    const dispatch = useDispatch()
    const {id}=useParams()

    const [loading,setLoading]=useState(false)


    useEffect(()=>{
      setLoading(true)
        getForts(id).then((data)=>dispatch(setForts(data)))
        .finally(()=>setLoading(false))
    },[id,dispatch])

    const nameForts=useSelector(seletFortsName)
    const imgForts=useSelector(selectImgForts)
    const descriptionForts = useSelector(selectDesForts)
    console.log(nameForts);

    if (loading) {
      return (
          <div className="loader-wrapper">
              <div className="spinner"></div>
          </div>
      );
  }
    return(
        <div className="page-bg">
        <div className="header-forts-container">
          <div className="header-forts">{nameForts}</div>
        </div>
        <div className="main-card">
            <div className="img-block">
                <img src={`data:image/pmg;base64,${imgForts}`} className="img-forts"/>
            </div>
            <div className="description-block">
                {descriptionForts}
      </div>
        </div>
        <div className="data-tours">
          <div >
            <p className="title-1">№ эксурксии</p>
          <input className="int"/>
          </div>
          <div>
            <p className="title-1">Количество мест</p>
          <input className="int"/>
          </div>
          <div>
            <p className="title-1">Место сбора</p>
          <input className="int"/>
          </div>
          <div >
            <p className="title-1">Дата экскурсии</p>
          <input className="int"/>
          </div>
          <div >
            <button className='btn-add'>Добавить</button>
          </div>
          <div><button className='btn-add-pic'>Добавить изображение</button></div>
        </div>
      </div>
    )
}
import { useParams } from "react-router-dom"
import { getForts } from "../../../api/get-forts"
import { useEffect,useState,useRef } from "react"
import { useDispatch } from "react-redux"
import { setForts } from "../../../action/set-forts"
import { useSelector } from "react-redux"
import { seletFortsName } from "../../../selectors/select-forts-name"
import { selectImgForts } from "../../../selectors/select-img-forts"
import { selectDesForts } from "../../../selectors/select-des-forts"
import { yupResolver } from "@hookform/resolvers/yup"
import { useForm } from "react-hook-form"
import { format } from 'date-fns'
import * as yup from 'yup'
import './forts-page.css'



const toursFormScheme=yup.object().shape({
  seats: yup
  .number()
  .min(1)
  .max(50)
  .integer('Только целые числа')
  .required('Обязательное поле'),
  date: yup
  .date()
  .min(new Date(),'Дата не может быть раньше сегодня')
  .typeError('Введите корректную дату')
  .required('Обязательное поле'),
  time: yup
  .string()
  .matches(/^([01]\d|2[0-3]):([0-5]\d)$/, 'Введите время в формате ЧЧ:ММ')
  .required('Выберите время экскурсии'),

  place: yup
  .string()
  .required('Заполните название улицы')
  .matches(/^[а-яА-Яa-zA-Z\s\-.]+$/, 'Название улицы может содержать только буквы, пробелы и дефис')
  .min(2, 'Минимум 2 символа')
  .max(30, 'Максимум 30 символов'),
})



export const FortsPage=()=>{
  const session=localStorage.getItem('session')

  const[image,setImage]=useState(null)
  const [previewImage, setPreviewImage] = useState(null);
  const fileInputRef = useRef(null);
  const [fileName, setFileName] = useState('');



  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.match('image.*')) {
      alert('Пожалуйста, выберите файл изображения');
      return;
    }
    setImage(file);  
    setFileName(file.name);
  const reader = new FileReader();
  reader.onloadend = () => {
    setPreviewImage(reader.result);
  };
  reader.readAsDataURL(file);
  }


  const sendImg= async()=>{
    const form = new FormData();
    form.append('image', image);

    const resolve = await fetch(`http://localhost:8000/forts/upload_image?fort_id=${id}`,{
      method: 'POST',
      body: form
    })
    return await resolve.json()

  }

  const handleUploadAndRefresh = async () => {
    await sendImg();
    const updatedFort = await getForts(id);
    dispatch(setForts(updatedFort)); 
  };



  const dispatch = useDispatch()
  const {id}=useParams()

  const {register,handleSubmit,formState:{errors}}=useForm({
    defaultValues:{
      seats: 1,
      date:'',
      time:'',
      place:''

    },
    resolver:yupResolver(toursFormScheme)
  })


  const onSubmited=async(data)=>{
    try {
      const formattedDate = format(new Date(data.date), 'yyyy-MM-dd');
      const dateWithTime = `${formattedDate} ${data.time}:00.000000`;
      
      const res = await fetch('http://localhost:8000/tours/add', {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'user-session': session,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'gathering_place': data.place,
          'tour_date': dateWithTime,
          'number_of_seats': data.seats,
          'fort_id': Number(id), 
        })
      });

      if(res.ok) alert('Экскурсия создана')
  
      if (!res.ok) {
        throw new Error('Ошибка при отправке данных');
      }
  
      return await res.json();
    } catch (error) {
      console.error('Ошибка:', error);
      throw error;
    }
  }

 
  const [loading,setLoading]=useState(false)

console.log('USE EFFECT CALL');
  useEffect(()=>{
    setLoading(true)
      getForts(id).then((data)=>{console.log(data)
        dispatch(setForts(data))})
      
      .finally(()=>setLoading(false))
  },[id,dispatch])

  const nameForts=useSelector(seletFortsName)
  const imgForts=useSelector(selectImgForts)
  const descriptionForts = useSelector(selectDesForts)


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
        <form className="data-tours" onSubmit={handleSubmit(onSubmited)}>
          <div>
            <p className="title-1" >Количество мест</p>
          <input className="int" min='1'type='number' name='seats' {...register('seats')}/>
          {errors.seats&&<div className="error">{errors.seats.message}</div>}
          </div>
          <div>
            <p className="title-1">Место сбора</p>
          <input className="int" type='place' name='place' {...register('place')}/>
          {errors.place&&<div className="error">{errors.place.message}</div>}
          </div>
          <div >
            <p className="title-1" >Дата экскурсии</p>
          <input className="int" type='date' name='date' {...register('date')}/>
          {errors.date&&<div className="error">{errors.date.message}</div>}
          </div>
          <div>
            <p className="title-1">Время экскурсии</p>
            <input className="int" type='time' name='time' {...register('time')}/>
            {errors.time&&<div className="error">{errors.time.message}</div>}
          </div>
            <div>
            <button className='btn-add' type="submit">Добавить</button>
            </div>
            <div>
            <button className='btn-add-pic' type="button" onClick={() => fileInputRef.current.click()}>Добавить изображение</button>
            <input ref={fileInputRef} type='file' accept="image/*" style={{display:'none'}} onChange={handleImageUpload}/>
            {previewImage && (
            <div className="info-img">
              {fileName}
              <button 
                type="button"
                onClick={() => {
                  setImage(null);
                  setPreviewImage(null);
                }}
                style={{marginLeft: '10px'}}
              >
                Удалить
              </button>
              <button
            type="button"
            onClick={handleUploadAndRefresh}
            style={{ marginLeft: '10px' }}
            disabled={!image}
        >
            Загрузить
        </button>
            </div>
          )}
            </div>
          </form>
      </div>
    )
}
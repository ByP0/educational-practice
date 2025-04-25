import { CardList } from "../list-tours/componets/card-list"
import { useLocation } from "react-router-dom"
import { useParams } from "react-router-dom"
import * as yup from 'yup'
import { useForm } from "react-hook-form"
import { Header } from "../../headers/header"
import { yupResolver } from "@hookform/resolvers/yup"
import { useNavigate } from "react-router-dom"
import { format } from 'date-fns'
import './editTourPage.css'



const toursFormScheme=yup.object().shape({
    seats: yup
    .number()
    .min(1)
    .max(50)
    .integer('Только целые числа')
    .notRequired(),
    date: yup
    .date()
    .min(new Date(),'Дата не может быть раньше сегодня')
    .typeError('Введите корректную дату')
    .notRequired(),
    time: yup
    .string()
    .matches(/^([01]\d|2[0-3]):([0-5]\d)$/, 'Введите время в формате ЧЧ:ММ')
    .notRequired(),
    place: yup
    .string()
    .notRequired()
    .matches(/^[а-яА-Яa-zA-Z\s\-.]+$/, 'Название улицы может содержать только буквы, пробелы и дефис')
    .min(2, 'Минимум 2 символа')
    .max(30, 'Максимум 30 символов'),
  })

export const EditTourPage=()=>{

    const session = localStorage.getItem('session')

    const {register,handleSubmit,formState:{errors}}=useForm({
        defaultValues:{
          seats: 1,
          date:'',
          time:'',
          place:''
    
        },
        resolver:yupResolver(toursFormScheme)
      })

   const{state}=useLocation()
   const tour = state?.tour
   const navigate = useNavigate()

   const {tourId}=useParams()

   const onSubmit=async(id,data)=>{
    try {
        console.log(data);
        const formattedDate = format(new Date(data.date), 'yyyy-MM-dd');
        const dateWithTime = `${formattedDate}+${' '}${data.time}:00.000000`;

        const response = await fetch(`http://localhost:8000/tours/patch?tour_id=${id}`, {
            method: 'PATCH',
            headers: {
                'accept': 'application/json',
                'user-session': session,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'gathering_place': data.place,
                'number_of_seats': data.seats,
                'tour_date': dateWithTime
            })
        });

        const result = await response.json();
        navigate('/list-tours',{state:{updateTour:result}})
        console.log('Success:', result);
    } catch (error) {
        console.error('Error:', error);
    }
   }

    return(
        <div>
            <Header/>
            <div className="edit-card-list">
                <CardList img={`data:${tour.image.content_type};base64,${tour.image.image_data}`}
                fortName={tour.fort_name} 
                numberOfSeats={tour.number_of_seats} 
                date={tour.tour_date}
                tourId={tour.tour_id}
                meetingPlace={tour.gathering_place} />
                <form className="edit-from" onSubmit={handleSubmit((data)=>onSubmit(tourId,data))}>
          <div>
            <p className="title-1" >Количество мест</p>
          <input className="int" min='1' type='number' name='seats' {...register('seats')}/>
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
            <button className='btn-add-edit' type="submit">Редактировать</button>
            </div>
          </form>
            </div>
        </div>
    )
}
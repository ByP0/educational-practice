import { CardList } from './componets/card-list'
import { useState,useEffect } from 'react'
import { useDispatch } from 'react-redux';
import { setUser } from '../../../action/set-user';
import './list-tours.css'
import { useNavigate,Link} from 'react-router-dom';
import { IoExitOutline } from "react-icons/io5";
import { RxHamburgerMenu } from "react-icons/rx";

export const ListTours=()=>{

    const session = localStorage.getItem('session')
    const[listTours,setListTours]=useState([])
    const [menuOpen,setMenuOpen]=useState(false)

    const dispatch=useDispatch()
    const navigate=useNavigate()
    console.log(session);

    useEffect(()=>{
        fetch(`http://localhost:8000/tours/my`,{
            headers: {
                'accept': 'application/json',
                'user-session': session
              }
        }).then(res=>res.json())
        .then((data)=>setListTours(data))
    },[session])

    const handleLogout=()=>{
        localStorage.removeItem('session')
        dispatch(setUser(null))
        navigate('/auth',{replace:true}) 
      }

 
    return(
        <div className="pg-list">
            <div className='header-list'>
            <button className='btn-menu'
                onClick={()=>setMenuOpen(!menuOpen)}>
                    <RxHamburgerMenu />
                    </button>
            <div className="title-list">Список экскурсий</div>
            </div>      
            <div className="card-list">
               <div>
                {listTours.map((item,tour_id)=>(
                    <CardList
                    fortName={item.fort_name}
                    tourId={item.tour_id}
                    numberOfSeats={item.number_of_seats}
                    meetingPlace={item.gathering_place}
                    date={item.tour_date}
                    img={`data:${item.image.content_type};base64,${item.image.image_data}`}
                    key={tour_id}
                  />
                ))}
               </div>
            </div>
            
            <div className={`mobile-menu${menuOpen ? ' open' : ''}`}>
                       <button className="close-btn" onClick={() => setMenuOpen(false)}>&times;</button>
                       <nav className='nav-links'>
                         <Link className='link-menu'to="/" onClick={()=>{
                            if(location.pathname==='/'){
                                setMenuOpen(false)
                            }
                         }}>Главная</Link>
                         <Link className='link-menu'to="/list-tours" onClick={()=>{
                            if(location.pathname==='/list-tours'){
                                setMenuOpen(false)
                            }
                         }} >Экскурсии</Link>
                         <Link className='link-menu'to="/#" onClick={()=>{
                            if(location.pathname==='/#'){
                                setMenuOpen(false)
                            }
                         }}>Контакты</Link>
                       </nav>
                       <button className='btn-exit' onClick={handleLogout}>Выход<IoExitOutline /></button>
                     </div>
        </div>
        
    )
}
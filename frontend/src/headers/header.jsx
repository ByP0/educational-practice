import './header.css'
import { RxHamburgerMenu } from "react-icons/rx";
import { IoIosSearch } from "react-icons/io";
import { IoExitOutline } from "react-icons/io5";
import{Link}from 'react-router-dom'
import { selectUserName } from '../../selectors/select-user-name';
import {useSelector} from 'react-redux'
import { useDispatch } from 'react-redux';
import { setUser } from '../../action/set-user';
 import { useNavigate } from 'react-router-dom';
 import { useState } from 'react';
 import { useLocation } from 'react-router-dom';
 


export const Header=()=>{

    const [menuOpen,setMenuOpen]=useState(false)

    
    
    const dispatch=useDispatch()
     const navigate=useNavigate()
     const location = useLocation()
     const isEditPage = location.pathname.includes("/edit");

    const user = useSelector(selectUserName)


    const handleLogout=()=>{
        localStorage.removeItem('session')
        dispatch(setUser(null))
        navigate('/auth',{replace:true}) 
      }
    return(
        <div className='header'>
            <div className='header-control'>
                <div className='menu'>       
                <button className='btn-menu'
                onClick={()=>setMenuOpen(!menuOpen)}>
                    <RxHamburgerMenu />
                    </button>
                <IoIosSearch  className='search'/>
                </div>
                <p className={`label ${isEditPage?'edit-page':''}`}>FortsTour</p>
                {!isEditPage&&(
                <>
                {user===null?(
                    <Link className='link-entry' to='/auth'><button className='btn-entrys'>Вход</button></Link>
                ):(
                    <>
                    <Link className='link-entry' to='/auth'><button className='btn-entrys' onClick={handleLogout}>Выход</button></Link>
                    </>
                )}
                </>
                )}
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
                       <button className='btn-exit' onClick={handleLogout}>Выход<IoExitOutline />{user}</button>
                     </div>
        </div>
    )
}
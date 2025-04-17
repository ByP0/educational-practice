import './header.css'
import { RxHamburgerMenu } from "react-icons/rx";
import { IoIosSearch } from "react-icons/io";
import{Link}from 'react-router-dom'

export const Header=()=>{
    return(
        <div className='header'>
            <div className='header-control'>
                <div className='menu'>
                <button className='btn-menu'><RxHamburgerMenu /></button>
                <IoIosSearch  className='search'/>
                </div>
                <p className="label">FortsTour</p>
                <Link className='link-entry' to='/auth'><button className='btn-entry'>Вход</button></Link>
            </div>
        </div>
    )
}
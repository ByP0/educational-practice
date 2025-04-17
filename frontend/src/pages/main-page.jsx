import { Header } from "../headers/header"
import { MdArrowBackIosNew } from "react-icons/md";
import { MdArrowForwardIos } from "react-icons/md";
import img1 from './images/image 1.png'
 import img2 from './images/image 2.png'
 import img3 from './images/image 3.png'
// import img4 from './images/image.png'
import img5 from './images/image 4.png'
import img6 from './images/image 5.png'
import img7 from './images/image 6.png'
import './main-page.css'
import { useState } from "react"


export const MainPage=()=>{

    const images=[img1,img5,img6,img7]

    const[currentImageIndex,setCurrentImageIndex]=useState(0)

    const nextImage=()=>{
        setCurrentImageIndex((prevIndex)=>(prevIndex+1) % images.length)
    }

    
    const prevImage=()=>{
        setCurrentImageIndex((prevIndex)=>(prevIndex-1+images.length)%images.length)
    }
    return(
        <div className="container">
            <Header/>
            <div className="imgs">
                <button onClick={(prevImage)} className="arrow left-arrow"><MdArrowBackIosNew/></button>
                <img  src={images[currentImageIndex]} alt='current'/>
                <button onClick={nextImage} className="arrow right-arrow"><MdArrowForwardIos/></button>
            </div>
            <div className="card">
                <div className="card-1">
                    <img src={img2} className="card-image"/>
                    <div className="card-content">
                    <h3>Форт № 1 «штайн»</h3>
                    </div>
                </div>
                <div className="card-2">
                    <img src={img3} className="card-image"/>
                    <div className="card-content">
                    <h3>Форт № 5 <br/>
                    «Король Фридрих-Вильгельм III»</h3>
                    </div>
                </div>
                <div className="card-3">
                    <img src={img3} className="card-image"/>
                    <div className="card-content">
                    <h3>Форт № 11 «Дёнхофф»</h3>
                    </div>
                </div>
            </div>
            

        </div>
    )
}
import { Header } from "../headers/header"
import { MdArrowBackIosNew } from "react-icons/md";
import { MdArrowForwardIos } from "react-icons/md";
import img1 from './images/image 1.png'
 import img2 from './images/image 2.png'
 import img3 from './images/image 3.png'
 import img4 from './images/image.png'
import img5 from './images/image 4.png'
import img6 from './images/image 5.png'
import './main-page.css'
import { useState } from "react"
import { Link } from "react-router-dom";
import { Card } from "./components/card";
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';


export const MainPage=()=>{

    const images=[img1,img5,img6]
    

    const[currentImageIndex,setCurrentImageIndex]=useState(0)
    const [direction, setDirection] = useState(0);

    const nextImage=()=>{
        setDirection(1);
            setCurrentImageIndex((prevIndex)=>(prevIndex+1) % images.length)
    }
    
    const prevImage=()=>{
        setDirection(-1);
            setCurrentImageIndex((prevIndex)=>(prevIndex-1+images.length)%images.length)
    }

    const variants = {
        enter: (dir) => ({
          x: dir > 0 ? 300 : -300,
          opacity: 0
        }),
        center: {
          x: 0,
          opacity: 1,
        },
        exit: (dir) => ({
          x: dir > 0 ? -300 : 300,
          opacity: 0
        })
      };
    
    return(
        <div className="container">
            <Header/>
            <div className="imgs">
                <button onClick={(prevImage)} className="arrow left-arrow"><MdArrowBackIosNew/></button>
                <AnimatePresence custom={direction} initial={false} mode="wait" >
            <motion.img
              key={currentImageIndex}
              src={images[currentImageIndex]}
              alt="current"
              custom={direction}
              variants={variants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.5 }}
              style={{
                objectFit: 'cover',
                width: '1300px',   
                height: '650px',        
                borderRadius: '12px', 
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
              }}
            />
          </AnimatePresence>
                <button onClick={nextImage} className="arrow right-arrow"><MdArrowForwardIos/></button>
            </div>
            <div className="card">
            <h2 className="title-create">Создай свою эксурксию!</h2>
                <Link className="link-card-1" to='/forts/1'>
                <Card img={img2} id={'1'} children='Форт № 1 «штайн»'/>
                </Link>
                <Link className="link-card-1" to='/forts/5'>
                <Card img={img3} id={'2'}><div className="card-title">Форт № 5 </div>
                    <div className="card-subtitle">«Король Фридрих-Вильгельм III»</div></Card>
                </Link>
                <Link className="link-card-1" to='/forts/11'>
                <Card img={img4} id={'3'} children='Форт № 11 «Дёнхофф»'/>
                </Link>
            </div>
        </div>
    )
}
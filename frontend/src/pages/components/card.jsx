import '../main-page.css'
export const Card = ({children,img,id})=>{
    return(
       
        <div className={`card-${id}`}>
                    <img src={img} className="card-image"/>
                    <div className="card-content">
                    <h3>{children}</h3>
                    </div>
        </div>
        
    )
}
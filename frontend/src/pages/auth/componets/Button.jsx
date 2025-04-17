import './components.css'

export const Button=({onClick,children,id})=>{
    return(
        <button className='btn'id={`btn-${id}`} onClick={onClick}>{children}</button>
    )
}
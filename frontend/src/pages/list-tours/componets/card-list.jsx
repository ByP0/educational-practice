import './card-list.css'
import { FaRegTrashCan } from "react-icons/fa6";
import { LuPencil } from "react-icons/lu";

export const CardList = ({ fortName, tourId,numberOfSeats, meetingPlace, date, img, id,onDelete,onEdit}) => {
    return (
      <div className={`card-1 card-${id}`}>
    <img src={img} alt={fortName} className="card-image" />
    <div className="card-content">
      <h2 className="fort-name">{fortName}</h2>
      <div className="card-info-grid">
        <div>
          <span className="label-1">Количество мест:</span>
          <span>{numberOfSeats}</span>
        </div>
        <div>
          <span className="label-1">Дата экскурсии:</span>
          <span>{date}</span>
        </div>
        <div>
          <span className="label-1">Номер экскурсии:</span>
          <span>{tourId}</span>
        </div>
        <div>
          <span className="label-1">Место сбора:</span>
          <span>{meetingPlace}</span>
        </div>
      </div>
    </div>
        <div>
          <button className='btn-delete' onClick={onDelete}><FaRegTrashCan/></button>
          <button className='btn-edit' onClick={onEdit}><LuPencil/></button>
        </div>
      </div>
    );
  };
  
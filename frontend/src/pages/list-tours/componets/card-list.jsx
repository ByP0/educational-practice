import './card-list.css'

export const CardList = ({ fortName, tourId,numberOfSeats, meetingPlace, date, img, id }) => {
    return (
      <div className={`card-${id} card-1`}>
        <img src={img} alt={fortName} className="card-image" />
        <div className="card-content">
          <h2 className="fort-name">{fortName}</h2>
          <div className="info-row-1">
            <div>Количество мест: <br />{numberOfSeats}</div>
          </div>
          <div className="info-row-2">
            <div>Номер экскурсии <br/>{tourId}</div>
            <div>Место сбора: <br />{meetingPlace}</div>
            <div>Дата экскурсии: <br />{date}</div>
          </div>
        </div>
      </div>
    );
  };
  
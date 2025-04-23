import './card-list.css'

export const CardList = ({ fortName, numberOfSeats, meetingPlace, date, img, id }) => {
    return (
      <div className={`card-${id}`}>
        <img src={img} alt={fortName} className="card-image" />
        <div className="card-content">
          <h2 className="fort-name">{fortName}</h2>
          <div className="info-row-1">
            <div>Количество мест: <br />{numberOfSeats}</div>
          </div>
          <div className="info-row-2">
            <div>Место сбора: <br />{meetingPlace}</div>
            <div>Дата экскурсии: <br />{date}</div>
          </div>
        </div>
      </div>
    );
  };
  
export const selectTourById = (state, tourId) => state.tours.find(tour => tour.tourId == tourId);



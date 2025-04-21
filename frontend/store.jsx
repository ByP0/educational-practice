import { userReducer } from "./reducers/userReducer";
import { fortsReducer } from "./reducers/fortsReducer";
import { createStore, applyMiddleware, compose, combineReducers } from "redux";
import { thunk } from "redux-thunk";

const reducer = combineReducers({
  user: userReducer,
  forts: fortsReducer
});

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export const store = createStore(
  reducer,
  composeEnhancers(applyMiddleware(thunk))
);

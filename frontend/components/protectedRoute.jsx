import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectUserName } from "../selectors/select-user-name";
import { useEffect } from "react";

export const ProtectedRoute = ({ children }) => {
    const navigate = useNavigate();
    const user = useSelector(selectUserName);
  
    useEffect(() => {
      if (!user) {
        navigate('/', { replace: true });
      }
    }, [user, navigate]);
  
    return children;
  }
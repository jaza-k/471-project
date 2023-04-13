import { Navigate, useLocation } from "react-router-dom";

export const setUserToken = (token) => {
  // set token in localStorage
  localStorage.setItem("userToken", token);
};

export const fetchToken = (token) => {
  // fetch the token
  return localStorage.getItem("userToken");
};

export function RequireToken({ children }) {
  let auth = fetchToken();
  let location = useLocation();

  if (!auth) {
    return <Navigate to="/" state={{ from: location }} />;
  }

  return children;
}

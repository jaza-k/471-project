import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/login.sass";
import key from "../assets/key.png";
import { ReactComponent as Logo } from "../assets/findmyride-logo.svg";
import { setUserToken } from "./Auth";
import axios from 'axios';

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  function handleClick() {
    navigate("/");
  }

  const handleLogin = () => {
    axios.post('http://localhost:8000/login', {
      email: email,
      password: password
    })
    .then(function (response) {
      if(response.data.token){       
        setUserToken(response.data.token)
        navigate("/dashboard");
      }
      else {
        alert("Error logging in");
      }
    })
    .catch(function (error) {
      console.log(error);
    });
  }


  return (
    <div className="App fade-in">
      <Logo onClick={handleClick} className="logo-bar" />
      <div className="page login-section">
        <img className="key-image" alt="" src={key} />
        <div className="page-column flex-align-center flex-column">
          <div>
            <div>
              <h1 className="login-heading">Welcome back</h1>
            </div>
            <div className="form">
              <form onSubmit={handleLogin}>
                <div>
                  <div className="input-container">
                    <label className="form-control mt-1">Email address</label>
                    <input
                      className="input-field"
                      placeholder="email@example.com"
                      type="text"
                      name="email"
                      required
                      onChange={(event) => setEmail(event.target.value)}
                    />
                  </div>

                  <div className="input-container">
                    <label>Password </label>
                    <input
                      className="input-field"
                      placeholder="*********"
                      type="password"
                      name="pass"
                      required
                      onChange={(event) => setPassword(event.target.value)}
                    />
                  </div>
                </div>
              </form>
            </div>
            <Link
              onClick={handleLogin}
              id="dashboard-button"
              className="button button-dark button-large"
            >
              Log in
            </Link>
            <div className="or-sign-up">Don't have an account?</div>
            <Link
              to="/signup"
              id="or-signup-button"
              className="button button-light button-large"
            >
              Sign up
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;

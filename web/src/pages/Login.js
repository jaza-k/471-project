import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/login.sass";
import key from "../assets/key.png";
import { ReactComponent as Logo } from "../assets/findmyride-logo.svg";
import PropTypes from 'prop-types';

function Login({ setToken }) {
  Login.propTypes = {
    setToken: PropTypes.func.isRequired
  };

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  function handleClick() {
    navigate("/");
  }

  const handleLogin = async e => {
    e.preventDefault();
    const token = await loginUser({
      email,
      password
    });
    setToken(token);
  }

  async function loginUser(credentials) {
    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      }).then(data => data.json());

      if (response.ok) {
        const result = await response.json();
        alert(result.message); // Display a success message
        navigate("/dashboard"); // Redirect to the dashboard page
      } else {
        alert("Error logging in");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

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
              <form onSubmit={loginUser}>
                <div>
                  <div className="input-container">
                    <label className="form-control mt-1">Email address</label>
                    <input
                      className="input-field"
                      placeholder="email@example.com"
                      type="text"
                      name="uname"
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

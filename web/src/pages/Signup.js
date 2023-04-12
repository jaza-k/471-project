import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/login.sass";
import lock from "../assets/lock.png";
import { ReactComponent as Logo } from "../assets/findmyride-logo.svg";

function Signup() {
  const [email, setEmail] = useState("");
  const [fname, setFname] = useState("");
  const [lname, setLname] = useState("");
  const [password, setPassword] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const navigate = useNavigate();

  function handleClick() {
    navigate("/");
  }

  const registerUser = async (event) => {
    event.preventDefault();
    const newUser = {
      fname: fname,
      lname: lname,
      email: email,
      password: password,
      city: city,
      country: country,
    };
  
    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser),
      });
  
      if (response.ok) {
        const result = await response.json();
        alert(result.message); // Display a success message
        navigate("/login"); // Redirect to the login page
      } else {
        alert("Error registering the user");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="App fade-in">
      <Logo onClick={handleClick} className="logo-bar" />
      <div className="page login-section">
        <img className="lock-image" alt="" src={lock} />
        <div className="page-column flex-align-center flex-column">
          <div>
            <div>
              <h1 className="login-heading">Create an account</h1>
              <div className="form">
                <form onSubmit={registerUser}>
                  <div className="names">
                    <div className="input-container">
                      <label className="form-control mt-1">First name </label>
                      <input
                        className="input-field first-name"
                        placeholder="John"
                        type="text"
                        name="fname"
                        required
                        onChange={(event) => setFname(event.target.value)}
                      />
                    </div>

                    <div className="input-container">
                      <label className="form-control mt-1">Last name </label>
                      <input
                        className="input-field last-name"
                        placeholder="Doe"
                        type="text"
                        name="lname"
                        required
                        onChange={(event) => setLname(event.target.value)}
                      />
                    </div>
                  </div>

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

                  <div className="location">
                    <div className="input-container">
                      <label className="form-control mt-1">City </label>
                      <input
                        className="input-field city"
                        placeholder="Calgary"
                        type="text"
                        name="city"
                        required
                        onChange={(event) => setCity(event.target.value)}
                      />
                    </div>

                    <div className="input-container">
                      <label className="form-control mt-1">Country </label>
                      <input
                        className="input-field country"
                        placeholder="Canada"
                        type="text"
                        name="country"
                        required
                        onChange={(event) => setCountry(event.target.value)}
                      />
                    </div>
                  </div>
                </form>
              </div>
              <Link
                id="signup-button-new"
                className="button button-dark button-large"
                onClick={registerUser}
              >
                Sign up
              </Link>
            </div>
            <div className="or-login">Already a user?</div>
            <Link
              to="/login"
              id="or-login-button"
              className="button button-light button-large"
            >
              Log into an account
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Signup;

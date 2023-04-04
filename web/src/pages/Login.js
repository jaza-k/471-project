import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/login.sass";
import key from "../assets/key.png"
import { ReactComponent as Logo } from "../assets/findmyride-logo.svg";

function Login() {
	const navigate = useNavigate();

	function handleClick() {
	  navigate("/");
	}

  const errors = {
    uname: "invalid username",
    pass: "invalid password"
  };
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  // User Login info
  const database = [
    {
      username: "user1",
      password: "pass1"
    },
    {
      username: "user2",
      password: "pass2"
    }
  ];
  const handleSubmit = (event) => {
    //Prevent page reload
    event.preventDefault();

    var { uname, pass } = document.forms[0];

    // Find user login info
    const userData = database.find((user) => user.username === uname.value);

    // Compare user info
    if (userData) {
      if (userData.password !== pass.value) {
        // Invalid password
        setErrorMessages({ name: "pass", message: errors.pass });
      } else {
        setIsSubmitted(true);
      }
    } else {
      // Username not found
      setErrorMessages({ name: "uname", message: errors.uname });
    }
  };
  const renderErrorMessage = (name) =>
  name === errorMessages.name && (
    <div className="error">{errorMessages.message}</div>
  );
    const renderForm = (
        <div className="form">
          <form onSubmit={handleSubmit}>
            <div>
            <div className="input-container">
              <label className="form-control mt-1">Email address</label>
              <input className="input-field" placeholder="email@example.com" type="text" name="uname" required />
              {renderErrorMessage("uname")}
            </div>

            <div className="input-container">
              <label>Password </label>
              <input className="input-field" placeholder="*********" type="password" name="pass" required />
              {renderErrorMessage("pass")}
            </div>

            </div>
           
          </form>
        </div>
      );
     
	return (
		<div className="App fade-in">
			<Logo onClick={handleClick} className="logo-bar"/>
			<div className="page login-section">
            <img className="key-image" src={key}/>
				<div className="page-column flex-align-center flex-column">
					<div>
						<div>
							<h1 className="login-heading">Welcome back</h1>
						</div>
                        {isSubmitted ? {handleClick} : renderForm}
							<Link to="/dashboard" id="dashboard-button" className="button button-dark button-large">
								Log in
							</Link>
                            <div className="or-sign-up">
                                Don't have an account?
                            </div>
                            <Link to="/signup" id="or-signup-button" className="button button-light button-large">
								Sign up
							</Link>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Login;
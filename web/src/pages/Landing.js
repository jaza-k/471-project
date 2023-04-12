import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/home.sass";
import { ReactComponent as Illustration1 } from "../assets/illustration1.svg";
import { ReactComponent as Illustration2 } from "../assets/illustration2.svg";
import { ReactComponent as Line } from "../assets/line.svg";
import { ReactComponent as Logo } from "../assets/findmyride-logo.svg";

function Landing() {
	const navigate = useNavigate();

	function handleClick() {
	  navigate("/");
	}

	return (
		<div className="App fade-in">
			<Logo onClick={handleClick} className="logo-bar"/>
			<div className="page homepage-section">
				<div>
					<Link to="/login" id="login-button" className="button button-light button-large">
						Log in
					</Link>
					</div>
					<div>
					<Link to="/signup" id="signup-button" className="button button-dark button-large">
						Sign up
					</Link>
				</div>
				<div className="page-column flex-align-center flex-column">
					<div>
						<div>
							<h1 className="page-heading">Lost your ride?</h1>
							<p className="subheading">
                            Whether it's your car, bicycle, or motorbike, Find My Ride scours the web for you to check if it's being sold online. If your vehicle turns up, we notify you right away of a possible match. All we need is a description of what's gone missing and let us do the rest. 
							</p>
							<div>
							<Link to="/signup" id="getstarted-button" className="button button-light button-large">
								Get started  ―  it's free
							</Link>
							</div>
						</div>
					</div>
					<Illustration1 className="illustration1"/>
				</div>
			</div>
		</div>
	);
}

export default Landing;
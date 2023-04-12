import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/login.sass";
import { ReactComponent as Gears1 } from "../assets/gears1.svg";
import { ReactComponent as Gears2 } from "../assets/gears2.svg";
import { ReactComponent as Logo } from "../assets/findmyride-logo.svg";

function Dashboard() {
	const navigate = useNavigate();

	function handleClick() {
	  navigate("/");
	}
     
	return (
		<div className="App">
			<Logo onClick={handleClick} className="logo-bar"/>
			<div className="page login-section">
				<div className="page-column flex-align-center flex-column">
					<div>
						<div>
                            <div>
                                <h1 className="hello-heading">Hello, user</h1>
                                
                                <p className="dashboard-subheading">
                                Manage your active searches here or create a new one.
                                </p>
						    </div>
                            <Gears1 className="gears1"/>
                            <Gears2 className="gears2"/>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Dashboard;
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/login.sass";
import "../styles/dashboard.sass";
import { ReactComponent as Gears1 } from "../assets/gears1.svg";
import { ReactComponent as Gears2 } from "../assets/gears2.svg";
import { ReactComponent as Logo } from "../assets/findmyride-logo.svg";

function Dashboard() {
	const [vehicleMake, setVehicleMake] = useState("");
	const [vehicleModel, setVehicleModel] = useState("");
	const [vehicleYear, setVehicleYear] = useState("");
	const [vehicleColor, setVehicleColor] = useState("");
	const [vehicleBodyType, setVehicleBodyType] = useState("");
	
	const [motorcycleMake, setMotorcycleMake] = useState("");
	const [motorcycleModel, setMotorcycleModel] = useState("");
	const [motorcycleYear, setMotorcycleYear] = useState("");
	const [motorcycleColor, setMotorcycleColor] = useState("");
	
  const navigate = useNavigate();
  const [showForm, setShowForm] = useState(""); // "vehicle" or "motorcycle"

  function handleClick() {
    navigate("/");
  }

  return (
    <div className="App">
      <Logo onClick={handleClick} className="logo-bar" />
      {/* <button type="button" onClick={signOut}>
        Sign Out
      </button> */}
      <div className="page login-section">
        <div className="page-column ">
          <div>
            <div>
              <div>
                <h1 className="hello-heading">Hello</h1>

                <p className="dashboard-subheading">
                  Manage your active searches here or create a new one.
                </p>

	  			<div className="searches-section">
				  <div className="active-search-section">
	  				<h3 className="new-search-heading">Your active searches</h3>
				</div>
				<div className="new-search-section">
                  <h3 className="new-search-heading">Create a new search</h3>
				  <div className="search-buttons">
					<button className="button button-dark button-large vehicle-button" onClick={() => setShowForm("vehicle")}>
						Vehicle
					</button>
					<button className="button button-dark button-large motorcycle-button" onClick={() => setShowForm("motorcycle")}>
						Motorcycle
					</button>
				  </div>

                  {showForm === "vehicle" && (
                    <form className="search-form">
                      <label>Make</label>
                      <input className="input-field search-input" type="text" />
                      <label>Model</label>
                      <input className="input-field search-input" type="text" />
                      <label>Year</label>
                      <input className="input-field search-input" type="text" />
                      <label>Colour</label>
                      <input className="input-field search-input" type="text" />
                      <label>Body type</label>
                      <input className="input-field search-input" type="text" />
                      <button className="button button-dark button-large create-vehicle-search" type="submit">Find my vehicle</button>
                    </form>
                  )}

                  {showForm === "motorcycle" && (
                    <form className="search-form">
                      <label>Make</label>
                      <input className="input-field search-input" type="text" />
                      <label>Model</label>
                      <input className="input-field search-input" type="text" />
                      <label>Year</label>
                      <input className="input-field search-input" type="text" />
                      <label>Colour</label>
                      <input className="input-field search-input" type="text" />
                      <button className="button button-dark button-large create-motorcycle-search" type="submit">Find my motorcycle</button>
                    </form>
                  )}
                </div>
				</div>
              </div>
              <Gears1 className="gears1" />
              <Gears2 className="gears2" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

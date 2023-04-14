import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
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
  
  const email = {
    email: "jaza"
  }

  const city = {
    city: "calgary"
  }

  const vehicleInfo = {
    searchType: "Vehicle",
    make: vehicleMake,
    model: vehicleModel,
    year: vehicleYear,
    color: vehicleColor,
    body_type: vehicleBodyType,
  }

  const VehicleData = [
    vehicleInfo,
    email,
    city
  ]

  const newVehicleSearch = async (event) => {
    event.preventDefault();
  
    try {
      const response = await fetch("http://localhost:8000/create-vehicle-search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(VehicleData),
      });
  
      if (response.ok) {
        const result = await response.json();
        alert(result.message); // Display a success message
        navigate("/login"); // Redirect to the login page
      } else {
        alert("Errorrrr");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };
  // const bodyFormDataV = new FormData();

  // VehicleData.forEach((item) => {
  //   bodyFormDataV.append('vehicleData[]', item);
  // });

  // const newVehicleSearch = () => {
  //   axios.post('http://localhost:8000/create-vehicle-search', VehicleData)
  //   .then(function (response) {
  //     if(response.data.token){       
  //       alert("Vehicle search created");
  //     }
  //     else {
  //       alert("Error");
  //     }
  //   })
  //   .catch(function (error) {
  //     console.log(error);
  //   });
  // }

  // const motorcycleInfo = {
  //   searchType: "Motorcycle",
  //   make: motorcycleMake,
  //   model: motorcycleModel,
  //   year: motorcycleYear,
  //   color: motorcycleColor,
  // }

  // const motorcycleData = [
  //   motorcycleInfo,
  //   email,
  //   city
  // ]
  
  // const bodyFormDataM = new FormData();

  // motorcycleData.forEach((item) => {
  //   bodyFormDataM.append('motorcycleData[]', item);
  // });

  // const newMotorcycleSearch = () => {
  //   axios.post('http://localhost:8000/create-motorcycle-search', bodyFormDataM)
  //   .then(function (response) {
  //     if(response.data.token){       
  //       alert("Motorcycle search created");
  //     }
  //     else {
  //       alert("Error");
  //     }
  //   })
  //   .catch(function (error) {
  //     console.log(error);
  //   });
  // }

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
                      <input className="input-field search-input" type="text" onChange={(event) => setVehicleMake(event.target.value)}/>
                      <label>Model</label>
                      <input className="input-field search-input" type="text" onChange={(event) => setVehicleModel(event.target.value)}/>
                      <label>Year</label>
                      <input className="input-field search-input" type="text" onChange={(event) => setVehicleYear(event.target.value)}/>
                      <label>Color</label>
                      <input className="input-field search-input" type="text" onChange={(event) => setVehicleColor(event.target.value)} />
                      <label>Body type</label>
                      <input className="input-field search-input" type="text" onChange={(event) => setVehicleBodyType(event.target.value)}/>
                      <button className="button button-dark button-large create-vehicle-search" type="button" onClick={newVehicleSearch}>Find my vehicle</button>
                    </form>
                  )}

                  {showForm === "motorcycle" && (
                    <form className="search-form">
                      <label>Make</label>
                      <input className="input-field search-input" type="text" onChange={(event) => setMotorcycleMake(event.target.value)} />
                      <label>Model</label>
                      <input className="input-field search-input" type="text" onChange={(event) => setMotorcycleModel(event.target.value)}/>
                      <label>Year</label>
                      <input className="input-field search-input" type="text" onChange={(event) => setMotorcycleYear(event.target.value)}/>
                      <label>Colour</label>
                      <input className="input-field search-input" type="text" onChange={(event) => setMotorcycleColor(event.target.value)}/>
                      <button className="button button-dark button-large create-motorcycle-search" type="button" >Find my motorcycle</button>
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

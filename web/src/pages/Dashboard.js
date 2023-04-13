import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/login.sass";
import { ReactComponent as Gears1 } from "../assets/gears1.svg";
import { ReactComponent as Gears2 } from "../assets/gears2.svg";
import { ReactComponent as Logo } from "../assets/findmyride-logo.svg";

function Dashboard() {
  const navigate = useNavigate();
  const [showForm, setShowForm] = useState(""); // "vehicle" or "motorcycle"

  function handleClick() {
    navigate("/");
  }

  return (
    <div className="App">
      <Logo onClick={handleClick} className="logo-bar" />
      <div className="page login-section">
        <div className="page-column flex-align-center flex-column">
          <div>
            <div>
              <div>
                <h1 className="hello-heading">Hello, user</h1>

                <p className="dashboard-subheading">
                  Manage your active searches here or create a new one.
                </p>
			
				<div className="new-search-section">
					<h3 className="new-search-heading">Create a new search</h3>
					<button onClick={() => setShowForm("vehicle")}>Vehicle</button>
					<button onClick={() => setShowForm("motorcycle")}>
					Motorcycle
					</button>

					{showForm === "vehicle" && (
					<form>
						<label>Make</label>
						<input type="text" />
						<label>Model</label>
						<input type="text" />
						<label>Year</label>
						<input type="text" />
						<label>Colour</label>
						<input type="text" />
						<label>Body type</label>
						<input type="text" />
						<button type="submit">Search</button>
					</form>
					)}

					{showForm === "motorcycle" && (
					<form>
						<label>Make</label>
						<input type="text" />
						<label>Model</label>
						<input type="text" />
						<label>Year</label>
						<input type="text" />
						<label>Colour</label>
						<input type="text" />
						<button type="submit">Search</button>
					</form>
					)}
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

import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import {RequireToken} from './Auth.js'

// pages
import Landing from "./Landing";
// import Workflow from "./Workflow";
import Login from "./Login";
import Dashboard from "./Dashboard";
import Signup from "./Signup";

function App() {
	return (
    <BrowserRouter>
      <Routes>
      <Route element={<Landing/>} path="/" exact />
        <Route element={<Login/>} path="/login" exact />
        <Route element={<Signup/>} path="/signup" exact />
        {/* <Route
          exact
          path="/dashboard"
          element={
            <RequireToken>
              <Dashboard />
            </RequireToken>
          }
        /> */}
        <Route element={<Dashboard/>} path="/dashboard" exact />
      </Routes>
    </BrowserRouter>
	);
}

export default App;
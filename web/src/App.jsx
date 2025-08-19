import React from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Buses from "./pages/Buses";
import RoutesPage from "./pages/Routes";
import Analytics from "./pages/Analytics";
import Sidebar from "./components/Sidebar.jsx";
import TopBar from "./components/TopBar.jsx";

function App() {
  const isAuthenticated = !!localStorage.getItem("token");
  const location = useLocation();
  const isLogin = location.pathname === "/login";

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      {!isLogin && <Sidebar />}
      <div
        style={{
          flexGrow: 1,
          marginLeft: !isLogin ? 240 : 0,
          background: "#f7f7f7",
          minHeight: "100vh",
        }}
      >
        {!isLogin && <TopBar />}
        <div style={{ padding: 24 }}>
          <Routes>
            <Route
              path="/login"
              element={
                isAuthenticated ? <Navigate to="/dashboard" /> : <Login />
              }
            />
            <Route
              path="/dashboard"
              element={
                isAuthenticated ? <Dashboard /> : <Navigate to="/login" />
              }
            />
            <Route
              path="/buses"
              element={isAuthenticated ? <Buses /> : <Navigate to="/login" />}
            />
            <Route
              path="/routes"
              element={
                isAuthenticated ? <RoutesPage /> : <Navigate to="/login" />
              }
            />
            <Route
              path="/analytics"
              element={
                isAuthenticated ? <Analytics /> : <Navigate to="/login" />
              }
            />
            <Route
              path="*"
              element={
                <Navigate to={isAuthenticated ? "/dashboard" : "/login"} />
              }
            />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;

// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header/Header";
import Menu from "./components/Menu/Menu";
import Home from "./components/Home/Home";
import "./App.css"; // Импортируем стили

const Queue = () => {
    return <h2>Очередь обработки</h2>;
};

const Help = () => {
    return <h2>О системе транскрибирования</h2>;
};

const Contact = () => {
    return <h2>Контакты</h2>;
};

const App = () => {
    return (
        <Router>
            <div>
                <Header />
                <Menu />
                <div className="app-container">
                    {" "}
                    {/* Применяем класс */}
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/queue" element={<Queue />} />
                        <Route path="/help" element={<Help />} />
                        <Route path="/contact" element={<Contact />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;

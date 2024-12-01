// src/components/Menu.js
import React from "react";
import { Link } from "react-router-dom";
import "./Menu.css";  // Импортируем файл стилей

const Menu = () => {
    return (
        <nav className="nav">
            <ul>
                <li>
                    <Link to="/">Главная</Link>
                </li>
                <li>
                    <Link to="/queue">Очередь обработки</Link>
                </li>
                <li>
                    <Link to="/help">О системе транскрибирования</Link>
                </li>
                <li>
                    <Link to="/contact">Контакты</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Menu;

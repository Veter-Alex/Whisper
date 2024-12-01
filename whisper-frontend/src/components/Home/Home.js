import React, { useState } from "react";
import "./Home.css"; // Импортируем CSS файл

// Пример имитации получения списка директорий и файлов
const directories = [
    {
        name: "Documents",
        subdirectories: [
            {
                name: "Work",
                files: ["report.docx", "budget.xlsx"],
                subdirectories: [
                    {
                        name: "Project A",
                        files: ["doc1.txt", "doc2.txt"]
                    }
                ]
            },
            {
                name: "Personal",
                files: ["letter.txt", "cv.pdf"],
            },
        ],
    },
    {
        name: "Downloads",
        subdirectories: [
            {
                name: "Images",
                files: ["photo1.jpg", "photo2.png"],
            },
            {
                name: "Videos",
                files: ["video1.mp4", "video2.mkv"],
            },
        ],
    },
];

const Home = () => {
    const [selectedDir, setSelectedDir] = useState(null); // Состояние для выбранной директории
    const [selectedFile, setSelectedFile] = useState(null); // Состояние для выбранного файла
    const [openDirs, setOpenDirs] = useState({}); // Состояние для отслеживания открытых/закрытых директорий

    // Функция для изменения состояния открытости/закрытости директории
    const toggleDirectory = (dirName) => {
        setOpenDirs((prevState) => ({
            ...prevState,
            [dirName]: !prevState[dirName], // Переключаем состояние открытости
        }));
    };

    const handleDirectorySelect = (dir) => {
        setSelectedDir(dir); // Обновляем выбранную директорию
        setSelectedFile(null); // Сбрасываем выбранный файл
    };

    const handleFileSelect = (file) => {
        setSelectedFile(file); // Обновляем выбранный файл
    };

    const renderSubdirectories = (dir, parentDirName) => {
        // Проверка наличия подкаталогов и их рендеринг
        if (!dir.subdirectories) return null;

        return (
            <ul className="subDirList">
                {dir.subdirectories.map((subDir, subIdx) => (
                    <li key={subIdx}>
                        <div>
                            <button
                                className="button"
                                onClick={() => {
                                    // Выбор вложенной директории
                                    handleDirectorySelect(subDir);
                                    toggleDirectory(`${parentDirName}-${subDir.name}`);
                                }}
                            >
                                {subDir.name}
                            </button>
                        </div>

                        {/* Рекурсивно отображаем вложенные подкаталоги только если они открыты */}
                        {openDirs[`${parentDirName}-${subDir.name}`] && renderSubdirectories(subDir, `${parentDirName}-${subDir.name}`)}
                    </li>
                ))}
            </ul>
        );
    };

    return (
        <div className="container">
            <div className="content-wrapper">
                {/* Боковой раздел для отображения директорий */}
                <div className="sidebar">
                    <h3>Директории</h3>
                    <ul className="dirList">
                        {directories.map((dir, idx) => (
                            <li key={idx}>
                                <div>
                                    <button
                                        className="button"
                                        onClick={() => {
                                            // Выбор директории и переключение её открытости
                                            handleDirectorySelect(dir);
                                            toggleDirectory(dir.name);
                                        }}
                                    >
                                        {dir.name}
                                    </button>
                                </div>

                                {/* Отображаем подкаталоги только если они открыты */}
                                {openDirs[dir.name] && renderSubdirectories(dir, dir.name)}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Основной раздел для отображения файлов выбранной директории */}
                <div className="mainContent">
                    {selectedDir ? (
                        <>
                            <h3>Файлы в {selectedDir.name}</h3>
                            <ul className="fileList">
                                {selectedDir.files && selectedDir.files.map((file, fileIdx) => (
                                    <li key={fileIdx}>
                                        <button
                                            className="button"
                                            onClick={() => handleFileSelect(file)}
                                        >
                                            {file}
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </>
                    ) : (
                        <p>Выберите директорию для отображения файлов.</p>
                    )}
                </div>
            </div>

            {/* Нижний раздел для отображения содержимого выбранного файла */}
            <div className="footer">
                {selectedFile ? (
                    <div>
                        <h4>Содержимое файла: {selectedFile}</h4>
                        <p>Здесь будет отображаться содержимое файла...</p>
                    </div>
                ) : (
                    <p>Выберите файл для просмотра содержимого.</p>
                )}
            </div>
        </div>
    );
};

export default Home;

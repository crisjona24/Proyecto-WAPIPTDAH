// Estilos
import { Link } from "react-router-dom";
import "../../styles/Registro.css"

export function CabeceraRegister() {
    return (
        <header className="header">
            <div className="left-section">
                <h1 className="title_header">
                    WAPIPTDAH
                </h1>
                <h5 className="subtitle_header">
                    Ayudamos a nuestros niños
                </h5>
            </div>
            <div className="right-section">
                <ul className="menu">
                    <li><Link to="/ver/datos">Conocenos</Link></li>
                    <li><Link to="/registro/contacto">Contactanos</Link></li>
                </ul>
            </div>
        </header>
    )
}
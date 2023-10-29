/* ****** COMPONENTE CONTENIDOS INDIVIDUALES *** */
// Estilos
//import "../../styles/Cabecera.css";
import "../../styles/Contenido_individual.css";
import "bootstrap/dist/css/bootstrap.min.css";
// Componentes
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from "react";
import { faBackward, faQuestion, fa1, fa2, fa3, fa4, faArrowRight, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
// Metodos
import { FormularioSeis } from '../registro/Formulario_individual_6'
import { VerificarUsuario } from "../../api/usuario.api"
import { ContenidoIndividualTodo } from "../../api/contenidoindividual.api";

export function ContenidoTipoSix({ context, slugContenido }) {
    // Verificacion de usuario
    const [tipoUsuario, setTipo] = useState([]);
    const navigate = useNavigate();
    const [error, setError] = useState("");


    /* *** Valores recuperados */
    const {
        nombre__contenido,
    } = context;

    // Verificar usuario
    const VerificarUser = async () => {
        try {
            const tipouser = await VerificarUsuario();
            if (tipouser.data.success) {
                setTipo(tipouser.data);
            } else {
                navigate('/login');
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al verificar usuario');
            }
        }
    }

    // Estado de los datos
    useEffect(() => {
        VerificarUser();
    }, []);

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div className="cabeza container">
            <div className="container pt-2">
                <div className="row col-md-12">
                    <div className="titulo__cabecera p-1">
                        <Link to={`/contenido/individual/all/${slugContenido}/`} className="boton__regreso btn btn-success">
                            <FontAwesomeIcon icon={faBackward} />
                        </Link>
                        <h2 className="display-6">
                            {nombre__contenido}
                        </h2>
                    </div>
                </div>
                <div className="row col-md-12">
                    <div className="titulo__ayuda">
                        <Link>
                            <span className="p-1">Necesitas ayuda</span>
                            <FontAwesomeIcon title="Regresar" className="boton__regreso btn btn-success" icon={faQuestion} />
                        </Link>
                    </div>
                </div>
                <div className="almacen__subtitulo row col-md-12 m-1">
                    <div className="subtitulo">
                        <h4 className="display-7">
                            {nombre__contenido}
                        </h4>
                    </div>
                </div>
                <div className="almacen__niveles row col-md-12">
                    <div className="contenedor__niveles mt-4 mb-4">



                    </div>
                </div>
                {/* Componente formulario */}
                <FormularioSeis context={context} usuario={tipoUsuario} slugContenido={slugContenido} />
                <div className="row col-md-12 mt-4 mb-2">

                    

                </div>

            </div>
        </div>
    )
}
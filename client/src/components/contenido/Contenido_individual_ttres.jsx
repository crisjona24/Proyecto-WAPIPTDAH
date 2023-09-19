/* ****** COMPONENTE CONTENIDOS INDIVIDUALES *** */
// Estilos
//import "../../styles/Cabecera.css";
import "../../styles/Contenido_individual.css";
import "bootstrap/dist/css/bootstrap.min.css";
// Componentes
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link, useNavigate } from 'react-router-dom';
import { useEffect, useState } from "react";
import { faBackward, faQuestion, fa1, fa2, fa3, fa4, faArrowRight, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
// Metodos
import { FormularioTres } from '../registro/Formulario_individual_3'
import { VerificarUsuario } from "../../api/usuario.api"

export function ContenidoTipoThree({ context, slugContenido }) {
    /* *** Valores recuperados */
    const {
        nombre__contenido,
    } = context;

    // Verificacion de usuario
    const [tipoUsuario, setTipo] = useState([]);
    const navigate = useNavigate();

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
                        <>
                            {
                                tipoUsuario.tipo === "paciente" &&
                                <div className="contenido__niveles">
                                    <div className="level textos">
                                        <Link> <FontAwesomeIcon title="Nivel de dificultad 1" icon={fa1} /> </Link>
                                    </div>
                                    <div className="level textos">
                                        <Link> <FontAwesomeIcon title="Nivel de dificultad 2" icon={fa2} /> </Link>
                                    </div>
                                    <div className="level textos">
                                        <Link> <FontAwesomeIcon title="Nivel de dificultad 3" icon={fa3} /> </Link>
                                    </div>
                                    <div className="level textos">
                                        <Link> <FontAwesomeIcon title="Nivel de dificultad 4" icon={fa4} /> </Link>
                                    </div>
                                </div>
                            }
                        </>
                    </div>
                </div>

                {/* Componente formulario */}
                <FormularioTres context={context} usuario={tipoUsuario} />
                {/* Fin componente formulario */}

                <div className="row col-md-12 mt-4 mb-2">
                    <>
                        {
                            tipoUsuario.tipo === "paciente" &&
                            <div className="bajo__cuerpo">
                                <div className="mt-2 mb-2">
                                    <Link className="boton__regreso btn btn-success">
                                        <FontAwesomeIcon title="Siguiente"
                                            icon={faArrowLeft} />
                                    </Link>

                                </div>
                                <div className="mt-2 mb-2">
                                    <Link className="boton__regreso btn btn-success">
                                        <FontAwesomeIcon title="Siguiente"
                                            icon={faArrowRight} />
                                    </Link>
                                </div>
                            </div>
                        }
                    </>
                </div>
            </div>
        </div>
    )
}
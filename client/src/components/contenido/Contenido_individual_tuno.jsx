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
import { FormularioUno } from '../registro/Formulario_individual_1';
import { VerificarUsuario } from "../../api/usuario.api";
import { ContenidoIndividualTodo } from "../../api/contenidoindividual.api";


export function ContenidoTipoOne({ context, slugContenido }) {
    // Verificacion de usuario
    const [tipoUsuario, setTipo] = useState([]);
    const navigate = useNavigate();
    const [error, setError] = useState("");

    // NUEVO
    const [contenidosI, setContenidos] = useState([]);
    const [slugSiguiente, setSlugSiguiente] = useState([]);
    const [slugAnterior, setSlugAnterior] = useState([]);
    let { slug2 } = useParams();
    let { slug } = useParams();
    // Obtener datos
    const cargarContenidosI = async () => {
        try {
            const cont = await ContenidoIndividualTodo(slug2);
            setContenidos(cont.data);
            console.log(cont.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al cargar contenidos');
            }
        }
    }

    // Buscar el slug siguiente y anterior
    const buscarSlug = () => {
        for (let i = 0; i < contenidosI.length; i++) {
            if (contenidosI[i].slug_contenido_individual === slug) {
                console.log(contenidosI[i].slug_contenido_individual);
                if (i === 0) {
                    setSlugAnterior("");
                    setSlugSiguiente(contenidosI[i + 1].slug_contenido_individual);
                    break;
                } else if (i === contenidosI.length - 1) {
                    setSlugAnterior(contenidosI[i - 1].slug_contenido_individual);
                    setSlugSiguiente("");
                    break;
                } else {
                    setSlugAnterior(contenidosI[i - 1].slug_contenido_individual);
                    setSlugSiguiente(contenidosI[i + 1].slug_contenido_individual);
                    break;
                }
            }
        }
    }

    useEffect(() => {
        cargarContenidosI();
    }, []);

    useEffect(() => {
        if (contenidosI.length > 1) {
            buscarSlug();
        } else {
            setSlugAnterior("");
            setSlugSiguiente("");
        }
    }, [contenidosI]);
    
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
                <FormularioUno context={context} usuario={tipoUsuario} slugContenido={slugContenido} />
                <div className="row col-md-12 mt-4 mb-2">

                    <>
                        {
                            tipoUsuario.tipo === "paciente" &&
                            <div className="bajo__cuerpo">
                                <div className="mt-2 mb-2">
                                    {
                                        slugAnterior !== "" &&
                                        <Link to={`/individual/${slugAnterior}/${slug2}/`} className="boton__regreso btn btn-success">
                                            <FontAwesomeIcon title="Anteior"
                                                icon={faArrowLeft} />
                                        </Link>
                                    }
                                </div>
                                <div className="mt-2 mb-2">
                                    {
                                        slugSiguiente !== "" &&
                                        <Link to={`/individual/${slugSiguiente}/${slug2}/`} className="boton__regreso btn btn-success">
                                            <FontAwesomeIcon title="Siguiente"
                                                icon={faArrowRight} />
                                        </Link>
                                    }

                                </div>
                            </div>
                        }
                    </>

                </div>

            </div>
        </div>
    )
}
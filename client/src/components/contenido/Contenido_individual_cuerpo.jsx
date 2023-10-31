/* ****** COMPONENTE CONTENIDOS INDIVIDUALES *** */
// Estilos
//import "../../styles/Cabecera.css";
import "../../styles/Contenido_individual.css";
import "../../styles/Varios.css";
import "bootstrap/dist/css/bootstrap.min.css";
// Componentes
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from "react";
import { faBackward, faQuestion, fa1, fa2, fa3, fa4, faArrowRight, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
// Metodos
import { FormularioUno } from '../registro/Formulario_individual_1';
import { FormularioDos } from '../registro/Formulario_individual_2';
import { FormularioTres } from '../registro/Formulario_individual_3';
import { Formulariocuatro } from '../registro/Formulario_individual_4';
import { FormularioCinco } from '../registro/Formulario_individual_5';
import { FormularioSeis } from '../registro/Formulario_individual_6';
import { FormularioSiete } from '../registro/Formulario_individual_7';
import { FormularioNueve } from '../registro/Formulario_individual_9';
import { FormularioDefault } from '../registro/Formulario_default';
import { VerificarUsuario } from "../../api/usuario.api";
import { ContenidoIndividualTodo } from "../../api/contenidoindividual.api";

export function ContenidoCuerpo({ context, slugContenido, tipoUsuarioP }) {
    // Valores recuperados de context
    const {
        nombre__contenido,
    } = context;

    // Verificacion de usuario
    const [tipoUsuario, setTipo] = useState([]);
    const navigate = useNavigate();
    const [error, setError] = useState("");
    let tipoFormulario;
    // NUEVO
    const [contenidosI, setContenidos] = useState([]);
    const [slugSiguiente, setSlugSiguiente] = useState("");
    const [slugAnterior, setSlugAnterior] = useState("");
    let { slug2 } = useParams();
    let { slug } = useParams();

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
                mostrarError("Error al verificar usuario")
            }
        }
    }

    // Estado de los datos del usuario
    useEffect(() => {
        VerificarUser();
    }, []);

    // Verificar tipo de contenido
    if (context.tipo) {
        // Usamos case para los casos de contenido
        switch (context.tipo) {
            case 'selecion_individual':
                tipoFormulario = <FormularioUno context={context} usuario={tipoUsuario} slugContenido={slugContenido} />;
                break;
            case "verdadero_falso":
                tipoFormulario = <FormularioDos context={context} usuario={tipoUsuario} slugContenido={slugContenido} />;
                break;
            case "selecion_multiple":
                tipoFormulario = <FormularioTres context={context} usuario={tipoUsuario} slugContenido={slugContenido} />;
                break;
            case "responder_preguntas":
                tipoFormulario = <Formulariocuatro context={context} usuario={tipoUsuario} slugContenido={slugContenido} />;
                break;
            case "pintar_imagen":
                tipoFormulario = <FormularioCinco context={context} usuario={tipoUsuario} slugContenido={slugContenido} />;
                break;
            case "seleccionar_imagen":
                tipoFormulario = <FormularioSeis context={context} usuario={tipoUsuario} slugContenido={slugContenido} />;
                break;
            case "cuento":
                tipoFormulario = <FormularioSiete context={context} usuario={tipoUsuario} slugContenido={slugContenido} />;
                break;
            case 'selecion_multiple_img':
                tipoFormulario = <FormularioNueve context={context} usuario={tipoUsuario} slugContenido={slugContenido} />;
                break;
            default:
                tipoFormulario = <FormularioDefault />;
                break;
        }
    }

    // Obtener datos
    const cargarContenidosI = async () => {
        try {
            // Verificar tipo de paciente
            if (tipoUsuarioP.tipo === "paciente") {
                const cont = await ContenidoIndividualTodo(slug2);
                setContenidos(cont.data);
                console.log(cont.data);
            }
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
        // Uso de maping para recorrer la lista de contenido consultada
        contenidosI.map((contenido, i) => {
            // Si el slug del contenido es igual al slug de la url en el momento
            if (contenido.slug_contenido_individual === slug) {
                // Si el indice es 0 o es el primer elemento, no hay anterior
                if (i === 0) {
                    setSlugAnterior("");
                    setSlugSiguiente(contenidosI[i + 1].slug_contenido_individual);
                    // Si el indice es el ultimo, no hay siguiente
                } else if (i === contenidosI.length - 1) {
                    setSlugAnterior(contenidosI[i - 1].slug_contenido_individual);
                    setSlugSiguiente("");
                    // Si no es ninguno de los anteriores, hay anterior y siguiente
                } else {
                    setSlugAnterior(contenidosI[i - 1].slug_contenido_individual);
                    setSlugSiguiente(contenidosI[i + 1].slug_contenido_individual);
                }
            }
        });
    }

    // Cargar contenidos completos
    useEffect(() => {
        cargarContenidosI();
    }, [context]);

    // Buscar slug
    useEffect(() => {
        if (contenidosI.length > 1) {
            buscarSlug();
        } else {
            setSlugAnterior("");
            setSlugSiguiente("");
        }
    }, [contenidosI]);

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
                {tipoFormulario}
                {/* Fin componente formulario */}

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

{/*
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
    */}
/* ****** COMPONENTE CONTENIDOS INDIVIDUALES *** */
// Estilos
import "../../styles/Cabecera.css";
import "../../styles/Contenido_individual.css";
import "bootstrap/dist/css/bootstrap.min.css";
// Componentes
import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link, useNavigate } from 'react-router-dom';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import Swal from 'sweetalert2';
// Metodos
import { CrearResultadoNew } from "../../api/resultado.api"

export function Formulariocuatro({ context, usuario, slugContenido }) {
    /* *** Valores recuperados *** */
    const {
        url__contenido, descripcion__contenido, identificador,
        tipo__contenido, slug
    } = context;
    const tipo = usuario.tipo;

    // Control de minutos
    const [startTime, setStartTime] = useState(null);
    const [tiempoDuracion, setTiempoDuracion] = useState(0);
    const intervalRef = useRef(null);
    // Control de tiempo
    let tiempoDeCarga;
    let tiempoActual;
    // Controles de contenido de estudio
    const empezarBtnRef = useRef(null);
    const verificarRef = useRef(null);
    const miContainerRef = useRef(null);
    const [respuestas, setRespuestas] = useState([]);
    const [tiempoTranscurrido__minutos, setMinutos] = useState(0);
    const [tiempoTranscurrido__segundos, setSegundos] = useState(0);
    const [contenidoHabilitado, setContenidoHabilitado] = useState(false);
    const [btnDisabled, setBtnDisabled] = useState(false);
    const [verificarBtnD, setVerificarBtnD] = useState(true);

    // Formulario    
    const [slug__, setSlug] = useState(slug);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Captura de valores para la respuesta
    useEffect(() => {
        // Controlar el botón "Empezar"
        setupEmpezarButton();
        // Control de minutos
        if (tiempoDuracion >= 40) {
            Swal.fire("Tiempo de resolución agotado", "", "warning");
            // Enviar el formulario
            enviarForm(new Event('submit'));
            // Si quieres, puedes detener el intervalo aquí
            clearInterval(intervalRef.current);
        }
        // Controlar los input checkbox
        const inputs = document.querySelectorAll('input[name="respuesta"]');
        inputs.forEach((input) => {
            input.addEventListener("input", () => {
                // Verificar si al menos uno de los checkboxes está seleccionado
                const isChecked = Array.from(inputs).some(
                    (input) => input.value != ""
                );
                // Habilitar o deshabilitar el botón "Verificar" según el resultado
                if (isChecked) {
                    tiempoActual = new Date();
                    let tiempoTranscurrido = tiempoActual - tiempoDeCarga;
                    // Convertir el tiempo a minutos y segundos
                    let { minutos, segundos } = convertirMilisegundosAMinutosYSegundos(tiempoTranscurrido);
                    setMinutos(minutos);
                    setSegundos(segundos);
                    setVerificarBtnD(false);
                } else {
                    setVerificarBtnD(true);
                }
            });
        });
        return () => {
            if (empezarBtnRef.current) {
                empezarBtnRef.current.removeEventListener("click", botonEmpezar);
            };
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            };
        };

    }, [tiempoDuracion, usuario]);

    // Controlar el botón "Empezar"
    const setupEmpezarButton = () => {
        if (empezarBtnRef.current) {
            empezarBtnRef.current.addEventListener("click", botonEmpezar);
            tiempoDeCarga = new Date();
        }
    };

    // Controlar el botón "Verificar"
    const botonEmpezar = () => {
        setContenidoHabilitado(true);
        setBtnDisabled(true);

        // Control de minutos
        setStartTime(Date.now());
        intervalRef.current = setInterval(() => {
            const now = Date.now();
            const timeDiff = now - startTime; // en milisegundos
            const minutesElapsed = Math.floor(timeDiff / (1000 * 60));
            setTiempoDuracion(minutesElapsed);
        }, 1000 * 60); // cada minuto
    };

    // Convertir milisegundos a minutos y segundos
    const convertirMilisegundosAMinutosYSegundos = (milisegundos) => {
        const segundos = Math.floor(milisegundos / 1000);
        const minutos = Math.floor(segundos / 60);
        const segundosRestantes = segundos % 60;
        return { minutos, segundos: segundosRestantes };
    }

    // Capturar los valores de los input
    const handleInputChange = (index, e) => {
        console.log(`Index: ${index}`, `Value: ${e.target.value}`);
        setRespuestas(prev => {
            const newRespuestas = [...prev];
            newRespuestas[index] = e.target.value;
            return newRespuestas;
        });
    };

    // Enviar los datos del formulario
    const enviarForm = async (e) => {
        if (e) {
            e.preventDefault();
        }
        try {
            const datos__post = {
                slug__,
                respuestas,
                tiempoTranscurrido__minutos,
                tiempoTranscurrido__segundos
            };
            console.log("Datos a enviar");
            console.log(datos__post);
            setVerificarBtnD(true);
            // Realizar la petición POST al servidor
            const response = await CrearResultadoNew(datos__post);
            if (response.data.success) {
                // Redireccionar a la página principal de contenido individual
                Swal.fire("Respuesta registrada", "", "success");
                navigate(`/contenido/individual/all/${slugContenido}/`);
            } else {
                if (response.data.error) {
                    mostrarError(response.data.error);
                } else {
                    mostrarError("Error al registrar resultado");
                }
            }
        } catch (err) {
            if (err.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError("Error al registrar resultado");
            }
        }
    };

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div style={{ margin: '0', padding: '0' }}>
            <div className="container row col-md-12">
                <div className="opciones__cuerpo">
                    <div className="alineacion__etiquetas d-flex flex-column justify-content-between">
                        <h5 className="card-title ml-2">
                            Ejercicio
                        </h5>
                        <h6 className="card-subtitle text-muted span mb-2" style={{ paddingLeft: '20px' }}>
                            Identificador: {identificador}</h6>
                        <h6 className="card-subtitle text-muted span mb-2" style={{ paddingLeft: '20px' }}>
                            Nivel: {tipo__contenido}</h6>
                    </div>
                    <div className="d-flex flex-row justify-content-between">
                        <>
                            {
                                tipo === "paciente" &&
                                <button ref={empezarBtnRef} disabled={btnDisabled} id="empezarBtn" type="button" className="btn btn-success"
                                    style={{ width: '100%', height: '40px', marginRight: '2%' }}>
                                    Resolver
                                </button>
                            }
                        </>
                        <span>
                            <Link className="btn btn-success" style={{ backgroundColor: '#0C2342' }}>
                                <FontAwesomeIcon icon={faStar} />
                            </Link>
                        </span>
                    </div>
                </div>
            </div>
            {error &&
                <div id="alert" className="alert alert-success" role="alert">
                    <h5 className="alert-heading">!Atención!</h5>
                    <p className="mb-0">{error}</p>
                </div>
            }
            <div className="container row col-md-12 mt-4">
                <div className="contenedor__cuerpo" id="miContainer" ref={miContainerRef}
                    style={{
                        pointerEvents: contenidoHabilitado ? 'auto' : 'none',
                        opacity: contenidoHabilitado ? 1 : 0.5
                    }}>
                    <div className="contenedor__cuerpo__division">
                        <div className="alineacion__etiquetas d-flex">
                            <>
                                {descripcion__contenido && descripcion__contenido.length > 1 && descripcion__contenido[0] &&
                                    <span className="span mt-3" style={{ color: 'rgb(0, 146, 99)' }}>
                                        Indicación: {descripcion__contenido[0]}</span>
                                }
                            </>
                        </div>
                        {/* <!-- Contenido de url--> */}
                        <div className="contenedor__imagen_tipo4" style={{ marginLeft: '5%' }}>
                            <div className="conten__tipo4 mt-4">
                                <div className="imagen_tipo4 mt-1 ml-5 mb-1 d-flex justify-content-center">
                                    <img style={{ width: '400px', height: '300px', border: '0.5px grey' }}
                                        src={url__contenido} alt="" />
                                </div>
                            </div>
                            <div className="card__cuerpo mt-2 pl-2">
                                <span className="referencia">
                                    Exámen: Prova de Aferição 1.º CEB, 2009, Portugal
                                </span>
                            </div>
                        </div>
                        <br />
                        {/* <!-- Contenido de url--> */}
                        <form onSubmit={enviarForm} style={{ marginLeft: '5%', marginTop: '1%' }}>
                            <div className="ml-3 pl-3">
                                <fieldset>
                                    <>
                                        {
                                            descripcion__contenido && descripcion__contenido.length > 1 &&
                                            descripcion__contenido[1].trim().startsWith("¿") &&
                                            descripcion__contenido.map((item, index) => {
                                                if (index > 0) {
                                                    return (
                                                        <div className="d-flex flex-column justify-content-between" key={index}>
                                                            <div className="form-group row ml-2">
                                                                <label htmlFor={`respuesta-${index}`} className="etiqueta col-sm-5 col-form-label" style={{ fontFamily: 'Pacifico cursive' }}>
                                                                    {item}</label>
                                                                <div className="col-sm-7">
                                                                    <input autoComplete="off" type="text" className="form-control w-75" id={`respuesta-${index}`}
                                                                        name="respuesta" style={{border: '1px solid #0C2342'}}
                                                                        onChange={(e) => handleInputChange(index - 1, e)} />
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )
                                                }
                                            })
                                        }
                                    </>
                                </fieldset>
                            </div>
                            {/* Eñ input que se envia */}
                            <input type="hidden" id="slug" name="slug" value={slug__} onChange={e => setSlug(e.target.value)} />

                            <div className="d-flex flex-column justify-content-between align-items-center mt-3">
                                <button type="submit" className="btn btn-success w-25"
                                    id="verificarBtn" ref={verificarRef} disabled={verificarBtnD}>
                                    !Listo!
                                </button>
                            </div>
                        </form>

                    </div>
                </div>
            </div>
        </div>
    )
}
// Estilos
//import "../../styles/Cabecera.css";
import "bootstrap/dist/css/bootstrap.min.css"
// Componentes
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
// Metodos
import { VerificarDominio, DominioIndividual } from "../../api/dominio.api";
import { PeticionIndividual } from "../../api/peticion.api";
import { Dominio } from "./general__tarjeta/TarjetaGeneral";
import { VerificarContenido, ContenidoIndividual } from "../../api/contenido.api";
import { Contenido } from "./general__tarjeta/TarjetaGeneral";
import { VerificarContenidoIndividual, ContenidoDatosIndividual } from "../../api/contenidoindividual.api";
import { Individual, Peticion, Paciente, Aplicacion } from "./general__tarjeta/TarjetaGeneral";
import { PacienteIndividual } from "../../api/usuario.api";


// Tarjeta de dominio
export function TarjetaDominio() {
    /* *** Control de datos *** */
    let { slug } = useParams();
    const [error, setError] = useState("");
    const [datos, setDatos] = useState([]);
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    // Datos
    const obtenerDatosDominio = async () => {
        // Promesa
        if (!token) {
            navigate('/login');
        }
        // Flujo normal
        try {
            const cont = await VerificarDominio(slug);
            if (cont.data.identificador) {
                // Obtener los datos del dominio
                const domi = await DominioIndividual(cont.data.identificador);
                setDatos(domi.data);
                console.log(domi.data)
            } else {
                if (cont.data.error) {
                    mostrarError(cont.data.error);
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al mostrar los datos de dominio');
            }
        }
    }

    // Obtener datos
    useEffect(() => {
        if (token) {
            obtenerDatosDominio();
        }
    }, [slug]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div>
            <>
                {
                    error &&
                    <div id="alert" className="alert alert-success" role="alert">
                        <h5 className="alert-heading">!Atención!</h5>
                        <span className="mb-0">{error}</span>
                    </div>
                }
                <Dominio datos={datos} />
            </>
        </div>
    )

}

// Tarjeta de contenido
export function TarjetaDatosContenido() {
    /* *** Control de datos *** */
    let { slug } = useParams();
    const [error, setError] = useState("");
    const [datos, setDatos] = useState([]);
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    // Datos
    const obtenerDatosContenido = async () => {
        // Promesa
        if (!token) {
            navigate('/login');
        }
        // Flujo normal
        try {
            const cont = await VerificarContenido(slug);
            console.log(cont.data)
            if (cont.data.identificador) {
                // Obtener los datos del dominio
                const domi = await ContenidoIndividual(cont.data.identificador);
                setDatos(domi.data);
                console.log(domi.data)
            } else {
                if (cont.data.error) {
                    mostrarError(cont.data.error);
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al mostrar los datos de contenido');
            }
        }
    }

    // Obtener datos
    useEffect(() => {
        if (token) {
            obtenerDatosContenido();
        }
    }, [slug]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div>
            <>
                {
                    error &&
                    <div id="alert" className="alert alert-success" role="alert">
                        <h5 className="alert-heading">!Atención!</h5>
                        <span className="mb-0">{error}</span>
                    </div>
                }
            </>
            <Contenido datos={datos} slug={slug} />
        </div>
    )

}

// Tarjeta de contenido individual
export function TarjetaDatosIndividual() {
    /* *** Control de datos *** */
    let { slug } = useParams();
    const [error, setError] = useState("");
    const [datos, setDatos] = useState([]);
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    // Datos
    const obtenerDatosContenidoI = async () => {
        // Promesa
        if (!token) {
            navigate('/login');
        }
        // Flujo normal
        try {
            const cont = await VerificarContenidoIndividual(slug);
            console.log(cont.data)
            if (cont.data.identificador) {
                // Obtener los datos del dominio
                const domi = await ContenidoDatosIndividual(cont.data.identificador);
                setDatos(domi.data);
            } else {
                if (cont.data.error) {
                    mostrarError(cont.data.error);
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al mostrar los datos de actividad');
            }
        }
    }

    useEffect(() => {
        if (token) {
            obtenerDatosContenidoI();
        }
    }, [slug]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div>
            <>
                {
                    error &&
                    <div id="alert" className="alert alert-success" role="alert">
                        <h5 className="alert-heading">!Atención!</h5>
                        <span className="mb-0">{error}</span>
                    </div>
                }
                <Individual datos={datos} slug={slug} />
            </>
        </div>
    )

}

// Tarjeta de peticion
export function TarjetaPeticion() {
    // Obtener el parametro de la URL
    let { id } = useParams();
    /* *** Form **** */
    const [datos, setDatos] = useState([]);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    // Obtener datos
    const obtenerDatosPeticion = async () => {
        try {
            // Buscar la peticion
            const cont = await PeticionIndividual(id);
            setDatos(cont.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al mostrar datos de petición');
            }
        }
    }

    // Use effect
    useEffect(() => {
        if (token) {
            obtenerDatosPeticion();
        }
    }, [id]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div>
            <>
                {
                    error &&
                    <div id="alert" className="alert alert-success" role="alert">
                        <h5 className="alert-heading">!Atención!</h5>
                        <span className="mb-0">{error}</span>
                    </div>
                }
                <Peticion datos={datos} />
            </>
        </div>
    )

}

// Tarjeta paciente
export function TarjetaPaciente() {
    // Obtener el parametro de la URL
    let { id } = useParams();
    /* *** Form **** */
    const [datosPaciente, setDatosP] = useState([]);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    // Obtener datos
    const obtenerDatosPaciente = async () => {
        try {
            // Buscar los datos de paciente
            const contP = await PacienteIndividual(id);
            setDatosP(contP.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al mostrar datos de petición');
            }
        }
    }

    // Use effect
    useEffect(() => {
        if (!token) {
            navigate('/login');
        } else {
            obtenerDatosPaciente();
        }
    }, [id]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div>
            <>
                {
                    error &&
                    <div id="alert" className="alert alert-success" role="alert">
                        <h5 className="alert-heading">!Atención!</h5>
                        <span className="mb-0">{error}</span>
                    </div>
                }
                <Paciente datosPaciente={datosPaciente} />
            </>
        </div>
    )
}

// Tarjeta de aplicacion
export function TarjetaAplicacion() {
    return (
        <div>
            <Aplicacion />
        </div>
    )
}
// Estilos
import "bootstrap/dist/css/bootstrap.min.css";
// Componentes
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from "react"
// Metodos
import { PeticionPendiente, PeticionAtendida, PeticionesUC } from "../../api/peticion.api"
import { ListaPeticion, ListaPeticionAtendida, ListaPeticionesUsuario } from "../general/ListaPeticion"
import { VerificarUsuario } from "../../api/usuario.api"

// Peticiones pendientes
export function PeticionLista() {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [peticiones, setPeticiones] = useState([]);
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;


    // Obtener datos
    const cargarPeticiones = async () => {
        try {
            // cargar datos de cursos
            const peticion = await PeticionPendiente(page);
            setPeticiones(peticion.data.results);
            if (peticion.data.results.length === 0) {
                setNumeropag(1);
            } else {
                setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
            }
            console.log("Son peticiones no atendidas")
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar peticiones');
            }
        }
    }

    // Estado de los datos
    useEffect(() => {
        cargarPeticiones();
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            cargarPeticiones();
        }, 15000);
        return () => clearInterval(interval);
    }, [page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Peticiones - Pendientes
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
            {error &&
                <div id="alert" className="alert alert-success" role="alert">
                    <h5 className="alert-heading">!Atención!</h5>
                    <p className="mb-0">{error}</p>
                </div>
            }
            {/* Table */}
            <ListaPeticion peticiones={peticiones} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )

}


// Peticiones atendidas
export function PeticionListaAtendi() {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [peticiones, setPeticiones] = useState([]);
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;

    // Obtener datos
    const cargarPeticiones = async () => {
        try {
            // cargar datos de cursos
            const peticion = await PeticionAtendida(page);
            setPeticiones(peticion.data.results);
            if (peticion.data.results.length === 0) {
                setNumeropag(1);
            } else {
                setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
            }
            console.log("Son peticiones atendidas")
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar peticiones');
            }
        }
    }

    useEffect(() => {
        cargarPeticiones();
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            cargarPeticiones();
        }, 15000);
        return () => clearInterval(interval);
    }, [page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Peticiones - Atendidas
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
            {error &&
                <div id="alert" className="alert alert-success" role="alert">
                    <h5 className="alert-heading">!Atención!</h5>
                    <p className="mb-0">{error}</p>
                </div>
            }
            {/* Table */}
            <ListaPeticionAtendida peticiones={peticiones} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )

}


// Peticiones de usuarios
export function PeticionListaUsuario() {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [peticiones, setPeticiones] = useState([]);
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;

    // Obtener datos
    const cargarPeticiones = async () => {
        try {
            // Verificar usuario
            const usuarioC = await VerificarUsuario();
            if (usuarioC.data.success) {
                // cargar datos de cursos
                const peticion = await PeticionesUC(usuarioC.data.identificador, page);
                setPeticiones(peticion.data.results);
                if (peticion.data.results.length === 0) {
                    setNumeropag(1);
                } else {
                    setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
                }
                console.log("Son peticiones de usuario")
            } else {
                navigate('/login');
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar peticiones de usuario');
            }
        }
    }

    // Estado de los datos
    useEffect(() => {
        cargarPeticiones();
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            cargarContenidosI();
        }, 3600000); // 1 hora
        return () => clearInterval(interval);
    }, [page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Peticiones de usuario
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
            {error &&
                <div id="alert" className="alert alert-success" role="alert">
                    <h5 className="alert-heading">!Atención!</h5>
                    <p className="mb-0">{error}</p>
                </div>
            }
            {/* Table */}
            <ListaPeticionesUsuario peticiones={peticiones} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )
}
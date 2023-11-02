// Estilos
import "bootstrap/dist/css/bootstrap.min.css";
// Componentes
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from "react";
import Swal from "sweetalert2";
import { Button } from "react-bootstrap";
// Metodos
import { PeticionPendiente, PeticionAtendida, PeticionesUC, PeticionporFecha, PeticionporRango } from "../../api/peticion.api"
import { ListaPeticion, ListaPeticionAtendida, ListaPeticionesUsuario } from "../general/ListaPeticion"
import { VerificarUsuario } from "../../api/usuario.api"
import { PeticionPendienteporFecha, PeticionPendienteporRango, PeticionAtendidaporFecha, PeticionAtendidaporRango } from "../../api/peticion.api"

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
    // Filtro de fecha
    const [fecha, setFecha] = useState("");
    const [limite, setLimite] = useState("");
    const [estadoBusqueda, setEstadoBusqueda] = useState(false);
    const [estadoBusquedaSel, setEstadoBusquedaSel] = useState(false);
    const [isTamanio, setIstamanio] = useState(false);

    // Obtener datos
    const cargarPeticiones = async () => {
        try {
            // cargar datos de cursos
            const peticion = await PeticionPendiente(page);
            setPeticiones(peticion.data.results);
            if (peticion.data.results.length === 0) {
                setNumeropag(1);
                setIstamanio(true);
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
        if (!estadoBusqueda) {
            cargarPeticiones();
        } else {
            buscarPeticionesTodas();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (!estadoBusqueda) {
                cargarPeticiones();
            } else {
                buscarPeticionesTodas();
            }
        }, 3600000); // 1 hora
        return () => clearInterval(interval);
    }, [estadoBusqueda, page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Metodo de busqueda
    const buscarPeticionesTodas = async () => {
        // Verificar campos vacíos
        if (isEmptyField(fecha)) {
            Swal.fire("Por favor ingrese el campo de fecha", "", "warning");
            return;
        }
        // Verificar fecha
        try {
            if (fecha !== "") {
                // cargar datos de cursos
                const peticion = await PeticionPendienteporFecha(fecha, page);
                if (peticion.data.results.length === 0) {
                    Swal.fire("No existen peticiones de esa fecha. Ingresa una válida", "", "warning");
                    resetearBusqueda();
                    return;
                } else {
                    setPeticiones(peticion.data.results);
                    setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
                    setEstadoBusqueda(true);
                }
            } else {
                cargarPeticiones();
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                Swal.fire("No existen peticiones de esa fecha. Ingresa una válida", "", "warning");
            }
        }
    }

    const buscarPeticionesRango = async () => {
        // Verificar fecha
        try {
            if (limite !== "") {
                // cargar datos de cursos
                const peticion = await PeticionPendienteporRango(limite, page);
                if (peticion.data.results.length === 0) {
                    Swal.fire("No existen peticiones de rango de días. Escoja otro", "", "warning");
                    resetearBusqueda();
                    return;
                } else {
                    setPeticiones(peticion.data.results);
                    setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
                    setEstadoBusquedaSel(true);
                }
            } else {
                cargarPeticiones();
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                Swal.fire("No existen peticiones en ese rango. Ingresa uno válido", "", "warning");
            }
        }
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setEstadoBusqueda(false);
        setEstadoBusquedaSel(false);
        setFecha("");
        setLimite("");
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Estado de los datos
    useEffect(() => {
        if (limite === "0") {
            cargarPeticiones();
        } else {
            buscarPeticionesRango();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (limite === "0") {
                cargarPeticiones();
            } else {
                buscarPeticionesRango();
            }
        }, 3600000); // 1 hora
        return () => clearInterval(interval);
    }, [limite, page]);

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
            {/* Para el filtro de fecha */}
            <div className="container mt-5 alienacion-externa">
                <div className="alineacion-lista-busqueda">
                    <div className="col-md-12">
                        <form>
                            <div className="row form-group">
                                <div className="col-2 d-flex justify-content-center mt-2">
                                    <label htmlFor="fecha" style={{ fontFamily: 'Pacifico' }}>Fecha</label>
                                </div>
                                <div className="col-9 d-flex flex-row">
                                    <input type="date" className="form-control" id="fecha"
                                        value={fecha} onChange={(e) => setFecha(e.target.value)} />
                                    <>
                                        {
                                            estadoBusqueda
                                                ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                                    X
                                                </Button>
                                                : <Button variant="success" className="my-2 my-sm-0" onClick={buscarPeticionesTodas} disabled={isTamanio}>
                                                    Buscar
                                                </Button>
                                        }
                                    </>
                                </div>

                            </div>
                        </form>
                    </div>
                </div>
                <div className="alineacion-lista-busqueda">
                    <div className="col-md-12">
                        <form>
                            <div className="row form-group">
                                <div className="col-2 d-flex justify-content-center mt-2">
                                    <label htmlFor="fecha" style={{ fontFamily: 'Pacifico' }}>Rango</label>
                                </div>
                                <div className="col-9 d-flex flex-row">
                                    <select name="fecha" id="fecha"
                                        value={limite} onChange={(e) => setLimite(e.target.value)} className="form-control"
                                    >
                                        <option value="0">Ninguno</option>
                                        <option value="7">Últimos 7 días</option>
                                        <option value="15">Últimos 15 días</option>
                                        <option value="30">Últimos 30 días</option>
                                        <option value="60">Últimos 60 días</option>
                                    </select>
                                    <>
                                        {
                                            estadoBusquedaSel
                                                ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                                    X
                                                </Button>
                                                : <> </>
                                        }
                                    </>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
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
    // Filtro de fecha
    const [fecha, setFecha] = useState("");
    const [limite, setLimite] = useState("");
    const [estadoBusqueda, setEstadoBusqueda] = useState(false);
    const [estadoBusquedaSel, setEstadoBusquedaSel] = useState(false);
    const [isTamanio, setIstamanio] = useState(false);

    // Obtener datos
    const cargarPeticiones = async () => {
        try {
            // cargar datos de cursos
            const peticion = await PeticionAtendida(page);
            setPeticiones(peticion.data.results);
            if (peticion.data.results.length === 0) {
                setNumeropag(1);
                setIstamanio(true);
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
        if (!estadoBusqueda) {
            cargarPeticiones();
        } else {
            buscarPeticionesTodasA();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (!estadoBusqueda) {
                cargarPeticiones();
            } else {
                buscarPeticionesTodasA();
            }
        }, 3600000); // 1 hora
        return () => clearInterval(interval);
    }, [estadoBusqueda, page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };


    // Metodo de busqueda
    const buscarPeticionesTodasA = async () => {
        // Verificar campos vacíos
        if (isEmptyField(fecha)) {
            Swal.fire("Por favor ingrese el campo de fecha", "", "warning");
            return;
        }
        // Verificar fecha
        try {
            if (fecha !== "") {
                // cargar datos de cursos
                const peticion = await PeticionAtendidaporFecha(fecha, page);
                if (peticion.data.results.length === 0) {
                    Swal.fire("No existen peticiones de esa fecha. Ingresa una válida", "", "warning");
                    resetearBusqueda();
                    return;
                } else {
                    setPeticiones(peticion.data.results);
                    setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
                    setEstadoBusqueda(true);
                }
            } else {
                cargarPeticiones();
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                Swal.fire("No existen peticiones de esa fecha. Ingresa una válida", "", "warning");
            }
        }
    }

    const buscarPeticionesRangoA = async () => {
        // Verificar fecha
        try {
            if (limite !== "") {
                // cargar datos de cursos
                const peticion = await PeticionAtendidaporRango(limite, page);
                if (peticion.data.results.length === 0) {
                    Swal.fire("No existen peticiones de rango de días. Escoja otro", "", "warning");
                    resetearBusqueda();
                    return;
                } else {
                    setPeticiones(peticion.data.results);
                    setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
                    setEstadoBusquedaSel(true);
                }
            } else {
                cargarPeticiones();
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                Swal.fire("No existen peticiones en ese rango. Ingresa uno válido", "", "warning");
            }
        }
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setEstadoBusqueda(false);
        setEstadoBusquedaSel(false);
        setFecha("");
        setLimite("");
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Estado de los datos
    useEffect(() => {
        if (limite === "0") {
            cargarPeticiones();
        } else {
            buscarPeticionesRangoA();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (limite === "0") {
                cargarPeticiones();
            } else {
                buscarPeticionesRangoA();
            }
        }, 3600000); // 1 hora
        return () => clearInterval(interval);
    }, [limite, page]);

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
            {/* Para el filtro de fecha */}
            <div className="container mt-5 alienacion-externa">
                <div className="alineacion-lista-busqueda">
                    <div className="col-md-12">
                        <form>
                            <div className="row form-group">
                                <div className="col-2 d-flex justify-content-center mt-2">
                                    <label htmlFor="fecha" style={{ fontFamily: 'Pacifico' }}>Fecha</label>
                                </div>
                                <div className="col-9 d-flex flex-row">
                                    <input type="date" className="form-control" id="fecha"
                                        value={fecha} onChange={(e) => setFecha(e.target.value)} />
                                    <>
                                        {
                                            estadoBusqueda
                                                ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                                    X
                                                </Button>
                                                : <Button variant="success" className="my-2 my-sm-0" onClick={buscarPeticionesTodasA} disabled={isTamanio}>
                                                    Buscar
                                                </Button>
                                        }
                                    </>
                                </div>

                            </div>
                        </form>
                    </div>
                </div>
                <div className="alineacion-lista-busqueda">
                    <div className="col-md-12">
                        <form>
                            <div className="row form-group">
                                <div className="col-2 d-flex justify-content-center mt-2">
                                    <label htmlFor="fecha" style={{ fontFamily: 'Pacifico' }}>Rango</label>
                                </div>
                                <div className="col-9 d-flex flex-row">
                                    <select name="fecha" id="fecha"
                                        value={limite} onChange={(e) => setLimite(e.target.value)} className="form-control"
                                    >
                                        <option value="0">Ninguno</option>
                                        <option value="7">Últimos 7 días</option>
                                        <option value="15">Últimos 15 días</option>
                                        <option value="30">Últimos 30 días</option>
                                        <option value="60">Últimos 60 días</option>
                                    </select>
                                    <>
                                        {
                                            estadoBusquedaSel
                                                ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                                    X
                                                </Button>
                                                : <> </>
                                        }
                                    </>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
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
    // Filtro de fecha
    const [fecha, setFecha] = useState("");
    const [limite, setLimite] = useState("");
    const [estadoBusqueda, setEstadoBusqueda] = useState(false);
    const [estadoBusquedaSel, setEstadoBusquedaSel] = useState(false);
    const [isTamanio, setIstamanio] = useState(false);

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
                    setIstamanio(true);
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
        if (!estadoBusqueda) {
            cargarPeticiones();
        } else {
            buscarPeticiones();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (!estadoBusqueda) {
                cargarPeticiones();
            } else {
                buscarPeticiones();
            }
        }, 3600000); // 1 hora
        return () => clearInterval(interval);
    }, [estadoBusqueda, page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Metodo de busqueda
    const buscarPeticiones = async () => {
        // Verificar campos vacíos
        if (isEmptyField(fecha)) {
            Swal.fire("Por favor ingrese el campo de fecha", "", "warning");
            return;
        }
        // Verificar fecha
        try {
            if (fecha !== "") {
                // Verificar usuario
                const usuarioC = await VerificarUsuario();
                if (usuarioC.data.success) {
                    // cargar datos de cursos
                    const peticion = await PeticionporFecha(fecha, usuarioC.data.identificador, page);
                    if (peticion.data.results.length === 0) {
                        Swal.fire("No existen peticiones de esa fecha. Ingresa una válida", "", "warning");
                        resetearBusqueda();
                        return;
                    } else {
                        setPeticiones(peticion.data.results);
                        setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
                        setEstadoBusqueda(true);
                    }
                } else {
                    navigate('/login');
                }
            } else {
                cargarPeticiones();
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                Swal.fire("No existen peticiones de esa fecha. Ingresa una válida", "", "warning");
            }
        }
    }

    const buscarPeticionesRango = async () => {
        // Verificar fecha
        try {
            if (limite !== "") {
                // Verificar usuario
                const usuarioC = await VerificarUsuario();
                if (usuarioC.data.success) {
                    // cargar datos de cursos
                    const peticion = await PeticionporRango(limite, usuarioC.data.identificador, page);
                    if (peticion.data.results.length === 0) {
                        Swal.fire("No existen peticiones de rango de días. Escoja otro", "", "warning");
                        resetearBusqueda();
                        return;
                    } else {
                        setPeticiones(peticion.data.results);
                        setNumeropag(Math.ceil(peticion.data.count / elementosPorPagina));
                        setEstadoBusquedaSel(true);
                    }
                } else {
                    navigate('/login');
                }
            } else {
                cargarPeticiones();
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                Swal.fire("No existen peticiones en ese rango. Ingresa uno válido", "", "warning");
            }
        }
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setEstadoBusqueda(false);
        setEstadoBusquedaSel(false);
        setFecha("");
        setLimite("");
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Estado de los datos
    useEffect(() => {
        if (limite === "0") {
            cargarPeticiones();
        } else {
            buscarPeticionesRango();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (limite === "0") {
                cargarPeticiones();
            } else {
                buscarPeticionesRango();
            }
        }, 3600000); // 1 hora
        return () => clearInterval(interval);
    }, [limite, page]);

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
            {/* Para el filtro de fecha */}
            <div className="container mt-4 alienacion-externa">
                <div className="alineacion-lista-busqueda">
                    <div className="col-md-12">
                        <form>
                            <div className="row form-group">
                                <div className="col-2 d-flex justify-content-center mt-2">
                                    <label htmlFor="fecha" style={{ fontFamily: 'Pacifico' }}>Fecha</label>
                                </div>
                                <div className="col-9 d-flex flex-row">
                                    <input type="date" className="form-control" id="fecha"
                                        value={fecha} onChange={(e) => setFecha(e.target.value)} />
                                    <>
                                        {
                                            estadoBusqueda
                                                ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                                    X
                                                </Button>
                                                : <Button variant="success" className="my-2 my-sm-0" onClick={buscarPeticiones} disabled={isTamanio}>
                                                    Buscar
                                                </Button>
                                        }
                                    </>
                                </div>

                            </div>
                        </form>
                    </div>
                </div>
                <div className="alineacion-lista-busqueda">
                    <div className="col-md-12">
                        <form>
                            <div className="row form-group">
                                <div className="col-2 d-flex justify-content-center mt-2">
                                    <label htmlFor="fecha" style={{ fontFamily: 'Pacifico' }}>Rango</label>
                                </div>
                                <div className="col-9 d-flex flex-row">
                                    <select name="fecha" id="fecha"
                                        value={limite} onChange={(e) => setLimite(e.target.value)} className="form-control"
                                    >
                                        <option value="0">Ninguno</option>
                                        <option value="7">Últimos 7 días</option>
                                        <option value="15">Últimos 15 días</option>
                                        <option value="30">Últimos 30 días</option>
                                        <option value="60">Últimos 60 días</option>
                                    </select>
                                    <>
                                        {
                                            estadoBusquedaSel
                                                ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                                    X
                                                </Button>
                                                : <> </>
                                        }
                                    </>
                                </div>

                            </div>
                        </form>
                    </div>
                </div>
            </div>
            {/* Table */}
            <ListaPeticionesUsuario peticiones={peticiones} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )
}
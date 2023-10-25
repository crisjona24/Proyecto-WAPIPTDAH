// Estilos
import "../../styles/Nivel.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Image, Button } from "react-bootstrap";
// Componentes
import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from "react";
import Swal from "sweetalert2";
// Metodos
import { VerificarUsuario, BusquedaPacientesCurso } from "../../api/usuario.api";
import { NivelListado } from "../../api/grado.api";
import { PacientesInscritos, VerificarCurso, CursoListado, CursosUsuarioComun, BusquedaCurso } from "../../api/curso.api";
import { ResultadosListado, PacientesResultados, ResultadosListaUsuario } from "../../api/resultado.api";
import { SalasUsuarioComun, SalaListado, SalasPaciente, BusquedaSalas, AccederSala } from "../../api/sala.api";
import { ReporteListado, ReporteListadoUsuarioComun, ReportesPaciente } from "../../api/reporte.api";
import { SalasUsuarioComunAtendidas } from "../../api/sala.api";

import { ListadodePacientes } from "../general/ListaPaciente";
import { OpcionesTecnico, OpcionesComun, OpcionesPaciente } from '../general/OpcionesNivel';
import { ListadodeCursos } from "../general/ListaCurso";
import { ListadodeReportes, ListadodeSala, ListadodeSalaPaciente, ListadodeResultado } from "../general/ListasEspecificas";


// Lista de niveles
export function NivelLista({ usuario }) {
    // Busqueda sala
    const [codigosala, setCodigo] = useState("");
    const [mostrarBusqueda, setMostrarBusqueda] = useState(false);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [niveles, setniveles] = useState([]);
    //const [localNiveles, setLocalNiveles] = useState(niveles);

    // Datos de nivel
    const cargarNiveles = async () => {
        try {
            // Obtenemos los datos de los niveles
            let domi = await NivelListado();
            setniveles(domi.data);
            //setLocalNiveles(niveles);
        } catch (err) {
            if (err.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al cargar los niveles');
            }
        }
    }

    // Manejo del estado de los datos
    useEffect(() => {
        if (!mostrarBusqueda) {
            cargarNiveles();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            cargarNiveles();
        }, 300000); // 5 minutos
        return () => clearInterval(interval);
    }, []);

    // Busqueda
    const busquedaContenido = async (e) => {
        // Verificar campos vacíos
        if (!isValidForm()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            let datos_obtenidos = await AccederSala(codigosala);
            if (datos_obtenidos.data.success) {
                console.log(datos_obtenidos.data);
                setMostrarBusqueda(true);
                navigate(`/individual/nuevo/${datos_obtenidos.data.slug}`);
            } else {
                if (datos_obtenidos.data.error) {
                    Swal.fire(datos_obtenidos.data.error, "", "warning");
                } else {
                    Swal.fire("No existen contenidos con ese código. Ingresa uno válido", "", "warning");
                }
            }
        } catch (error) {
            Swal.fire("No existen contenidos con ese código. Ingresa uno válido", "", "warning");
        }
    }

    // Campos vacios
    const isValidForm = () => {
        if (
            !codigosala ||
            codigosala === 0
        ) {
            return false;
        }
        return true;
    }

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
                    usuario.tipo === "paciente" &&
                    <div className="d-flex flex-row mb-3">
                        <div className="card-body">
                            <form className="d-flex flex-row" >
                                <div className="input-group">
                                    <input type="search" className="form-control rounded" placeholder="Inserta código de sala"
                                        aria-label="Search" aria-describedby="search-addon" value={codigosala}
                                        onChange={e => {
                                            const entrada = e.target.value;
                                            const numero = Number(entrada);
                                            if (numero >= 0 || entrada === "") {
                                                setCodigo(entrada);
                                            }
                                        }
                                        } />
                                    <>
                                        {
                                            !mostrarBusqueda
                                                ? <Button variant="success" className="my-2 my-sm-0"
                                                    onClick={() => {
                                                        Swal.fire({
                                                            title: '¿Está seguro que desea acceder a la actividad?',
                                                            text: "Si, acceder",
                                                            icon: 'info',
                                                            showCancelButton: true,
                                                            confirmButtonColor: '#3085d6',
                                                            cancelButtonColor: '#d33',
                                                            confirmButtonText: 'Sí',
                                                        }).then(async (result) => {
                                                            if (result.isConfirmed) {
                                                                await busquedaContenido();
                                                            }
                                                        })
                                                    }}
                                                >
                                                    Buscar
                                                </Button>
                                                :
                                                <></>
                                        }
                                    </>
                                </div>
                            </form>
                        </div>
                    </div>
                }
            </>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Niveles TDAH
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
            <>
                {error &&
                    <div id="alert" className="alert alert-success" role="alert">
                        <h5 className="alert-heading">!Atención!</h5>
                        <p className="mb-0">{error}</p>
                    </div>
                }

                {
                    niveles.map((nivel) => (
                        <div className="contenedor-listado__nivel" key={nivel.id}>
                            <div className="contenedor-nombre__nivel">
                                <li style={{ listStyle: 'none' }}>
                                    <h6 style={{ fontFamily: 'Pacifico' }}>Grado TDAH: {nivel.descripcion_grado}</h6>
                                </li>
                            </div>
                            <div className="contenedor__nivel">
                                <div className="contenedor-datos__nivel">
                                    <div className="card__nivel">
                                        <div className="textos__nivel d-flex flex-column justify-content-between">
                                            <Image src="/img/abeja_ivbapx.jpg"
                                                className="imagen__nivel" />
                                        </div>
                                    </div>
                                    <div className="card__nivel">
                                        <div className="textos__nivel d-flex flex-column justify-content-between">
                                            <li>
                                                <h3 className="titulo__dato"> Nombre </h3>
                                            </li>
                                            <li className="valor__dato"> {nivel.nombre_nivel} </li>
                                        </div>
                                    </div>
                                    <div className="card__nivel">
                                        <div className="textos__nivel d-flex flex-column justify-content-between">
                                            <li>
                                                <h3 className="titulo__dato"> Categorías </h3>
                                            </li>
                                            <li className="valor__dato"> {nivel.numero_categorias} </li>
                                        </div>
                                    </div>
                                    <div className="card__nivel">
                                        <div className="textos__nivel d-flex flex-column justify-content-between">
                                            <li>
                                                <h3 className="titulo__dato"> Dificultad </h3>
                                            </li>
                                            <li className="valor__dato font-weight-normal"> {nivel.grado_dificultad} </li>
                                        </div>
                                    </div>
                                </div>

                                <>
                                    {
                                        usuario.tipo === "tecnico" &&
                                        <OpcionesTecnico nivel={nivel} />
                                    }
                                    {
                                        usuario.tipo === "comun" &&
                                        <OpcionesComun nivel={nivel} />
                                    }
                                    {
                                        usuario.tipo === "paciente" &&
                                        <OpcionesPaciente nivel={nivel} />
                                    }
                                </>

                            </div>
                        </div>

                    ))
                }
                <hr style={{ color: '#0C2342' }} />
                {
                    usuario.tipo === "tecnico" &&

                    <div className="cabeza__Nivel">
                        <div className="container">
                            <div className="row">
                                <div className="col-md-12">
                                    <h4 className="display-7 mt-2">
                                        Reportes
                                    </h4>
                                </div>
                            </div>
                        </div>
                    </div>
                }
            </>

        </div>
    )
}


// Lista de pacientes asociadas a un curso
export function PacienteListado() {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    // Capturar slug
    let { slug } = useParams();
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [pacientes, setPacientes] = useState([]);
    const token = localStorage.getItem('token');
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;
    // Busqueda
    const [nombrebuscarP, setNombreBuscarP] = useState("");
    const [mostrarBusqueda, setMostrarBusqueda] = useState(false);
    const [isTamanio, setIstamanio] = useState(false);
    const [entradaValida, setEntradavaldia] = useState(true);

    const cargarPacientes = async () => {
        try {
            // Verificar curso
            const curso = await VerificarCurso(slug);
            if (curso.data.identificador) {
                // Cargar datos de pacientes
                let paciente = await PacientesInscritos(curso.data.identificador, page);
                setPacientes(paciente.data.results);
                if (paciente.data.results.length === 0) {
                    setIstamanio(true);
                    setNumeropag(1);
                } else {
                    setNumeropag(Math.ceil(paciente.data.count / elementosPorPagina));
                }
            } else {
                mostrarError('Error al cargar los pacientes inscritos');
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar los pacientes inscritos');
            }
        }
    }

    // Manejo del estado de los datos
    useEffect(() => {
        if (token && !mostrarBusqueda) {
            cargarPacientes();
        } else if (token && mostrarBusqueda) {
            busquedaPaciente();
        }
    }, [slug, page, mostrarBusqueda]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Busqueda
    const busquedaPaciente = async () => {
        // Verificar campos vacíos
        if (isEmptyField(nombrebuscarP)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Entrada
        if (!entradaValida) {
            Swal.fire("Por favor ingrese el formato: Nombre Apellido", "", "warning");
            return;
        }
        // Flujo normal
        try {
            const busqueda_paciente = await BusquedaPacientesCurso(nombrebuscarP, slug, page);
            if (busqueda_paciente.data.results.length === 0) {
                setNumeropag(1);
                Swal.fire("No existe un paciente con ese nombre. Ingresa un nombre válido", "", "warning");
                return;
            } else {
                setPacientes(busqueda_paciente.data.results);
                setNumeropag(Math.ceil(busqueda_paciente.data.count / elementosPorPagina));
                setMostrarBusqueda(true);
            }
        } catch (error) {
            Swal.fire("No existe un paciente con ese nombre. Ingresa un nombre válido", "", "warning");
        }
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setMostrarBusqueda(false);
        setNombreBuscarP("");
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Funcion para validar la entreada
    const cambioEntrada = (e) => {
        const value = e.target.value;
        setNombreBuscarP(value);

        if (!validarEntrada(value)) {
            setEntradavaldia(false);
        } else {
            setEntradavaldia(true);
        }
    };

    const validarEntrada = (value) => {
        const generar = /^[a-zA-Z]+ [a-zA-Z]+$/;
        return generar.test(value);
    };

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Pacientes inscritos
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
            <div className="mt-4 container" style={{ height: '50px', borderRadius: '10px' }}>
                <div className="d-flex flex-row justify-content-left w-100" style={{ alignItems: 'center', marginLeft: '1px' }}>
                    <a className="m-2" style={{ fontFamily: 'Pacifico' }}>Buscar</a>
                    <form className="d-flex flex-row justify-content-between w-50">
                        <input className="form-control mr-sm-2 w-100" type="search" name="nombre" id="nombre"
                            placeholder="Nombre de paciente.." aria-label="Search" value={nombrebuscarP}
                            onChange={cambioEntrada} disabled={isTamanio} />
                        <>
                            {
                                mostrarBusqueda
                                    ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                        X
                                    </Button>
                                    : <Button variant="success" className="my-2 my-sm-0" onClick={busquedaPaciente} disabled={isTamanio}>
                                        Ir
                                    </Button>
                            }
                        </>
                    </form>
                </div>
            </div>
            {/* Table */}
            <ListadodePacientes pacientes={pacientes} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )

}


// Lista de resultados
export function ResultadoLista({ usuario }) {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [resultados, setResultados] = useState([]);
    const [nombrebuscar, setNombreBuscar] = useState("");
    // Validaciones
    const [mostrarBusqueda, setMostrarBusqueda] = useState(false);
    const [isTamanio, setIstamanio] = useState(false);
    const [entradaValida, setEntradavaldia] = useState(true);
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;

    // Obtener resultados
    const cargarResultados = async () => {
        try {
            // Verificar usuario
            const usuario_dat = await VerificarUsuario();
            if (usuario_dat.data.success) {
                if (usuario_dat.data.tipo === "comun") {
                    let resultado = await ResultadosListaUsuario(usuario_dat.data.identificador, page);
                    setResultados(resultado.data.results);
                    if (resultado.data.results.length === 0) {
                        setIstamanio(true);
                        setNumeropag(1);
                    } else {
                        setNumeropag(Math.ceil(resultado.data.count / elementosPorPagina));
                    }
                } else {
                    // Cargar datos de resultados
                    let resultado_n = await ResultadosListado(page);
                    setResultados(resultado_n.data.results);
                    if (resultado_n.data.results.length === 0) {
                        setIstamanio(true);
                        setNumeropag(1);
                    } else {
                        setNumeropag(Math.ceil(resultado_n.data.count / elementosPorPagina));
                    }
                }
            } else {
                if (usuario_dat.data.error) {
                    Swal.fire("Hubo un problema para identificar el usuario", "", "warning");
                    navigate('/login')
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar los resultados');
            }
        }
    }

    // Manejo del estado de los datos
    useEffect(() => {
        if (!mostrarBusqueda) {
            cargarResultados();
        } else {
            busquedaResultado();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (!mostrarBusqueda) {
                cargarResultados();
            } else {
                busquedaResultado();
            }
        }, 1200000); // 20 minutos
        return () => clearInterval(interval);

    }, [mostrarBusqueda, page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Busqueda
    const busquedaResultado = async () => {
        // Verificar campos vacíos
        if (isEmptyField(nombrebuscar)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Entrada
        if (!entradaValida) {
            Swal.fire("Por favor ingrese el formato: Nombre Apellido", "", "warning");
            return;
        }
        // Flujo normal
        try {
            const datos_obtenidos = await PacientesResultados(nombrebuscar, page);
            if (datos_obtenidos.data.results.length === 0) {
                setNumeropag(1);
                Swal.fire("No existen resultados con ese nombre de paciente. Ingresa un nombre válido", "", "warning");
                return;
            } else {
                setResultados(datos_obtenidos.data.results);
                setNumeropag(Math.ceil(datos_obtenidos.data.count / elementosPorPagina));
                setMostrarBusqueda(true);
            }
        } catch (error) {
            Swal.fire("No existen resultados con ese nombre de paciente. Ingresa un nombre válido", "", "warning");
        }
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setMostrarBusqueda(false);
        setNombreBuscar("");
    }

    // Funcion para validar la entreada
    const cambioEntrada = (e) => {
        const value = e.target.value;
        setNombreBuscar(value);

        if (!validarEntrada(value)) {
            setEntradavaldia(false);
        } else {
            setEntradavaldia(true);
        }
    };

    const validarEntrada = (value) => {
        const generar = /^[a-zA-Z]+ [a-zA-Z]+$/;
        return generar.test(value);
    };

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Resultados generales
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
            <div className="mt-4 container" style={{ height: '50px', borderRadius: '10px' }}>
                <div className="d-flex flex-row justify-content-left w-100" style={{ alignItems: 'center', marginLeft: '1px' }}>
                    <a className="m-2" style={{ fontFamily: 'Pacifico' }}>Buscar</a>
                    <form className="d-flex flex-row justify-content-between w-50">
                        <input className="form-control mr-sm-2 w-100" type="search" name="nombre" id="nombre"
                            placeholder="Nombre del paciente.." aria-label="Search" value={nombrebuscar}
                            onChange={cambioEntrada} disabled={isTamanio} />
                        <>
                            {
                                mostrarBusqueda
                                    ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                        X
                                    </Button>
                                    : <Button variant="success" className="my-2 my-sm-0" onClick={busquedaResultado} disabled={isTamanio}>
                                        Ir
                                    </Button>
                            }
                        </>
                    </form>
                </div>
            </div>
            {/* Table */}
            <ListadodeResultado resultados={resultados} usuario={usuario} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )

}


// Lista de cursos
export function CursoLista() {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo de los datos
    const [cursos, setCursos] = useState([]);
    const token = localStorage.getItem('token');
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;
    // Busqueda
    const [nombrebuscar, setNombreBuscar] = useState("");
    const [mostrarBusqueda, setMostrarBusqueda] = useState(false);
    const [isTamanio, setIstamanio] = useState(false);

    // Datos de curso
    const cargarCursos = async () => {
        try {
            // Verificar usuario
            const usuario_dat = await VerificarUsuario();
            if (usuario_dat.data.success) {
                if (usuario_dat.data.tipo === "comun") {
                    const curso = await CursosUsuarioComun(page);
                    setCursos(curso.data.results);
                    console.log("Son los cursos especificos")
                    if (curso.data.results.length === 0) {
                        setNumeropag(1);
                        setIstamanio(true);
                    } else {
                        setNumeropag(Math.ceil(curso.data.count / elementosPorPagina));
                    }
                } else {
                    const curso_tecnico = await CursoListado(page);
                    setCursos(curso_tecnico.data.results);
                    console.log("Son los cursos generales")
                    if (curso_tecnico.data.results.length === 0) {
                        setNumeropag(1);
                        setIstamanio(true);
                    } else {
                        setNumeropag(Math.ceil(curso_tecnico.data.count / elementosPorPagina));
                    }
                }
            } else {
                if (usuario_dat.data.error) {
                    Swal.fire("Hubo un problema para identificar el usuario", "", "warning");
                    navigate('/login')
                }
            }
        } catch (err) {
            if (err.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar cursos');
            }
        }
    }

    // Estado de los datos
    useEffect(() => {
        if (token && !mostrarBusqueda) {
            cargarCursos();
        } else if (token && mostrarBusqueda) {
            busquedaCurso();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (token && !mostrarBusqueda) {
                cargarCursos();
            } else if (token && mostrarBusqueda) {
                busquedaCurso();
            }
        }, 300000); // 5 minutos
        return () => clearInterval(interval);
    }, [mostrarBusqueda, page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Busqueda
    const busquedaCurso = async () => {
        // Verificar campos vacíos
        if (isEmptyField(nombrebuscar)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            const datos_obtenidos = await BusquedaCurso(nombrebuscar, page);
            if (datos_obtenidos.data.results.length === 0) {
                setNumeropag(1);
                Swal.fire("No existen cursos con ese nombre. Ingresa un nombre válido", "", "warning");
                return;
            } else {
                setCursos(datos_obtenidos.data.results);
                setNumeropag(Math.ceil(datos_obtenidos.data.count / elementosPorPagina));
                setMostrarBusqueda(true);
            }
        } catch (error) {
            Swal.fire("No existen cursos con ese nombre. Ingresa un nombre válido", "", "warning");
        }
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setMostrarBusqueda(false);
        setNombreBuscar("");
    }

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Cursos
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
            <div className="mt-4 container" style={{ height: '50px', borderRadius: '10px' }}>
                <div className="d-flex flex-row justify-content-left w-100" style={{ alignItems: 'center', marginLeft: '1px' }}>
                    <a className="m-2" style={{ fontFamily: 'Pacifico' }}>Buscar</a>
                    <form className="d-flex flex-row justify-content-between w-50">
                        <input className="form-control mr-sm-2 w-100" type="search" name="nombre" id="nombre"
                            placeholder="Nombre del curso.." aria-label="Search" value={nombrebuscar}
                            onChange={e => setNombreBuscar(e.target.value)} disabled={isTamanio} />
                        <>
                            {
                                mostrarBusqueda
                                    ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                        X
                                    </Button>
                                    : <Button variant="success" className="my-2 my-sm-0" onClick={busquedaCurso} disabled={isTamanio}>
                                        Ir
                                    </Button>
                            }
                        </>
                    </form>
                </div>
            </div>
            {/* Table */}
            <ListadodeCursos cursos={cursos} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )

}



// Lista de salas creadas
export function SalaLista({ usuario }) {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [salas, setSalas] = useState([]);
    const [isTamanio, setIstamanio] = useState(false);
    const [nombrebuscar, setNombreBuscar] = useState("");
    const [mostrarBusqueda, setMostrarBusqueda] = useState(false);
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;

    // Obtener resultados
    const cargarSala = async () => {
        try {
            // Verificar usuario
            const usuario_dat = await VerificarUsuario();
            if (usuario_dat.data.success) {
                if (usuario_dat.data.tipo === "tecnico") {
                    const sala_tecnico = await SalaListado(page);
                    setSalas(sala_tecnico.data.results);
                    if (sala_tecnico.data.results.length === 0) {
                        setIstamanio(true);
                        setNumeropag(1);
                    } else {
                        setNumeropag(Math.ceil(sala_tecnico.data.count / elementosPorPagina));
                    }
                } else {
                    const sala = await SalasUsuarioComun(usuario_dat.data.identificador, page);
                    setSalas(sala.data.results);
                    if (sala.data.results.length === 0) {
                        setIstamanio(true);
                        setNumeropag(1);
                    } else {
                        setNumeropag(Math.ceil(sala.data.count / elementosPorPagina));
                    }
                }
            } else {
                if (usuario_dat.data.error) {
                    Swal.fire("Hubo un problema para identificar el usuario", "", "warning");
                    navigate('/login')
                }
            }
        } catch (err) {
            if (err.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar las salas');
            }
        }
    }

    // Manejo del estado de los datos
    useEffect(() => {
        if (!mostrarBusqueda) {
            cargarSala();
        } else {
            busquedaClick();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (!mostrarBusqueda) {
                cargarSala();
            } else {
                busquedaClick();
            }
        }, 1200000); // 20 minutos
        return () => clearInterval(interval);

    }, [mostrarBusqueda, page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Busqueda
    const busquedaClick = async () => {
        // Verificar campos vacíos
        if (isEmptyField(nombrebuscar)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            const busqueda_sala = await BusquedaSalas(nombrebuscar, page);
            if (busqueda_sala.data.results.length === 0) {
                setNumeropag(1);
                Swal.fire("No existen salas con ese nombre. Ingresa un nombre válido", "", "warning");
                return;
            } else {
                setSalas(busqueda_sala.data.results);
                setNumeropag(Math.ceil(busqueda_sala.data.count / elementosPorPagina));
                setMostrarBusqueda(true);
            }
        } catch (error) {
            Swal.fire("No existe una sala con ese nombre. Ingresa un nombre válido", "", "warning");
        }
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setMostrarBusqueda(false);
        setNombreBuscar("");
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Salas creadas
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
            <div className="mt-4 container" style={{ height: '50px', borderRadius: '10px' }}>
                <div className="d-flex flex-row justify-content-left w-100" style={{ alignItems: 'center', marginLeft: '1px' }}>
                    <a className="m-2" style={{ fontFamily: 'Pacifico' }}>Buscar</a>
                    <form className="d-flex flex-row justify-content-between w-50">
                        <input className="form-control mr-sm-2 w-100" type="search" name="nombre" id="nombre"
                            placeholder="Nombre de sala.." aria-label="Search" value={nombrebuscar}
                            onChange={e => setNombreBuscar(e.target.value)} disabled={isTamanio} />
                        <>
                            {
                                mostrarBusqueda
                                    ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                        X
                                    </Button>
                                    : <Button variant="success" className="my-2 my-sm-0" onClick={busquedaClick} disabled={isTamanio}>
                                        Ir
                                    </Button>
                            }
                        </>
                    </form>
                </div>
            </div>
            {/* Table */}
            <ListadodeSala salas={salas} usuario={usuario} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )
}



// Lista de salas de paciente
export function SalaPacienteLista() {
    // Busqueda sala
    const [codigosala, setCodigo] = useState("");
    const [mostrarBusqueda, setMostrarBusqueda] = useState(false);
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [salas, setSalas] = useState([]);
    const token = localStorage.getItem('token');
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;

    // Obtener resultados
    const cargarSalaPaciente = async () => {
        try {
            // Verificar usuario
            const usuario_dat = await VerificarUsuario();
            if (usuario_dat.data.success) {
                // Cargar datos de salas
                const sala = await SalasPaciente(usuario_dat.data.identificador, page);
                setSalas(sala.data.results);
                if (sala.data.results.length === 0) {
                    setNumeropag(1);
                } else {
                    setNumeropag(Math.ceil(sala.data.count / elementosPorPagina));
                }
            } else {
                if (usuario_dat.data.error) {
                    Swal.fire("Hubo un problema para identificar el usuario", "", "warning");
                    navigate('/login')
                }
            }

        } catch (err) {
            if (err.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar las salas');
            }
        }
    }

    // Manejo del estado de los datos
    useEffect(() => {
        if (token) {
            cargarSalaPaciente();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            cargarSalaPaciente();
        }, 1200000); // 20 minutos
        return () => clearInterval(interval);

    }, [page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Busqueda
    const busquedaContenido = async (e) => {
        // Verificar campos vacíos
        if (!isValidForm()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            let datos_obtenidos = await AccederSala(codigosala);
            if (datos_obtenidos.data.success) {
                console.log(datos_obtenidos.data);
                setMostrarBusqueda(true);
                navigate(`/individual/nuevo/${datos_obtenidos.data.slug}`);
            } else {
                if (datos_obtenidos.data.error) {
                    Swal.fire(datos_obtenidos.data.error, "", "warning");
                } else {
                    Swal.fire("No existen contenidos con ese código. Ingresa uno válido", "", "warning");
                }
            }
        } catch (error) {
            Swal.fire("No existen contenidos con ese código. Ingresa uno válido", "", "warning");
        }
    }

    // Campos vacios
    const isValidForm = () => {
        if (
            !codigosala ||
            codigosala === 0
        ) {
            return false;
        }
        return true;
    }

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Salas de estudiante
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
            {/* Busqueda de actividad mediante el codigo */}
            <div className="d-flex flex-row mt-4">
                <div className="card-body">
                    <form className="d-flex flex-row" >
                        <div className="input-group" style={{marginLeft:'8%', width: '85%'}}>
                            <input type="search" className="form-control rounded" placeholder="Inserta código de sala"
                                aria-label="Search" aria-describedby="search-addon" value={codigosala}
                                onChange={e => {
                                    const entrada = e.target.value;
                                    const numero = Number(entrada);
                                    if (numero >= 0 || entrada === "") {
                                        setCodigo(entrada);
                                    }
                                }
                                } />
                            <>
                                {
                                    !mostrarBusqueda
                                        ? <Button variant="success" className="my-2 my-sm-0"
                                            onClick={() => {
                                                Swal.fire({
                                                    title: '¿Está seguro que desea acceder a la actividad?',
                                                    text: "Si, acceder",
                                                    icon: 'info',
                                                    showCancelButton: true,
                                                    confirmButtonColor: '#3085d6',
                                                    cancelButtonColor: '#d33',
                                                    confirmButtonText: 'Sí',
                                                }).then(async (result) => {
                                                    if (result.isConfirmed) {
                                                        await busquedaContenido();
                                                    }
                                                })
                                            }}
                                        >
                                            Buscar
                                        </Button>
                                        :
                                        <></>
                                }
                            </>
                        </div>
                    </form>
                </div>
            </div>
            {/* Table */}
            <ListadodeSalaPaciente salas={salas} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )
}



// Lista de salas creadas
export function SalaListaAtendidas({ usuario }) {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [salas, setSalas] = useState([]);
    const [isTamanio, setIstamanio] = useState(false);
    const [nombrebuscar, setNombreBuscar] = useState("");
    const [mostrarBusqueda, setMostrarBusqueda] = useState(false);
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;

    // Obtener resultados
    const cargarSalaAtendi = async () => {
        try {
            // Verificar usuario
            const usuario_dat = await VerificarUsuario();
            if (usuario_dat.data.success) {
                let sala = await SalasUsuarioComunAtendidas(usuario_dat.data.identificador, page);
                setSalas(sala.data.results);
                if (sala.data.results.length === 0) {
                    setIstamanio(true);
                    setNumeropag(1);
                } else {
                    setNumeropag(Math.ceil(sala.data.count / elementosPorPagina));
                }
            } else {
                if (usuario_dat.data.error) {
                    Swal.fire("Hubo un problema para identificar el usuario", "", "warning");
                    navigate('/login')
                }
            }

        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar las salas');
            }
        }
    }

    // Manejo del estado de los datos
    useEffect(() => {
        if (!mostrarBusqueda) {
            cargarSalaAtendi();
        } else {
            busquedaDeSala();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (!mostrarBusqueda) {
                cargarSalaAtendi();
            } else {
                busquedaDeSala();
            }
        }, 1200000); // 20 minutos
        return () => clearInterval(interval);

    }, [mostrarBusqueda, page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Busqueda
    const busquedaDeSala = async () => {
        // Verificar campos vacíos
        if (isEmptyField(nombrebuscar)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            const busqueda_sala = await BusquedaSalas(nombrebuscar, page);
            if (busqueda_sala.data.results.length === 0) {
                setNumeropag(1);
                Swal.fire("No existen salas con ese nombre. Ingresa un nombre válido", "", "warning");
                return;
            } else {
                setSalas(busqueda_sala.data.results);
                setNumeropag(Math.ceil(busqueda_sala.data.count / elementosPorPagina));
                setMostrarBusqueda(true);
            }
        } catch (error) {
            Swal.fire("No existe una sala con ese nombre. Ingresa un nombre válido", "", "warning");
        }
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setMostrarBusqueda(false);
        setNombreBuscar("");
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Salas atendidas
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
            <div className="mt-4 container" style={{ height: '50px', borderRadius: '10px' }}>
                <div className="d-flex flex-row justify-content-left w-100" style={{ alignItems: 'center', marginLeft: '1px' }}>
                    <a className="m-2" style={{ fontFamily: 'Pacifico' }}>Buscar</a>
                    <form className="d-flex flex-row justify-content-between w-50">
                        <input className="form-control mr-sm-2 w-100" type="search" name="nombre" id="nombre"
                            placeholder="Nombre de sala.." aria-label="Search" value={nombrebuscar}
                            onChange={e => setNombreBuscar(e.target.value)} disabled={isTamanio} />
                        <>
                            {
                                mostrarBusqueda
                                    ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                        X
                                    </Button>
                                    : <Button variant="success" className="my-2 my-sm-0" onClick={busquedaDeSala} disabled={isTamanio}>
                                        Ir
                                    </Button>
                            }
                        </>
                    </form>
                </div>
            </div>
            {/* Table */}
            <ListadodeSala salas={salas} usuario={usuario} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )
}



// Lista de reportes
export function ReporteLista({ usuario }) {
    // Paginacion
    const [page, setPage] = useState(1);
    // Fin paginacion
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Manejo del estado de los datos
    const [reportes, setReportes] = useState([]);
    const [numeroPag, setNumeropag] = useState(1);
    const elementosPorPagina = 8;
    // BUSQUEDA
    const [nombrebuscar, setNombreBuscar] = useState("");
    const [isTamanio, setIstamanio] = useState(false);
    const [mostrarBusqueda, setMostrarBusqueda] = useState(false);
    const [entradaValida, setEntradavaldia] = useState(true);

    // Obtener resultados
    const cargarReporte = async () => {
        try {
            // Verificar usuario
            const usuario_dat = await VerificarUsuario();
            if (usuario_dat.data.tipo === "tecnico") {
                const reporte_tecnico = await ReporteListado(page);
                setReportes(reporte_tecnico.data.results);
                if (reporte_tecnico.data.results.length === 0) {
                    setIstamanio(true);
                    setNumeropag(1);
                } else {
                    setNumeropag(Math.ceil(reporte_tecnico.data.count / elementosPorPagina));
                }
            } else {
                const reporte = await ReporteListadoUsuarioComun(usuario_dat.data.identificador, page);
                setReportes(reporte.data.results);
                console.log("Son los reportes especificos")
                if (reporte.data.results.length === 0) {
                    //setIstamanio(true);
                    setNumeropag(1);
                } else {
                    setNumeropag(Math.ceil(reporte.data.count / elementosPorPagina));
                }
            }
        } catch (err) {
            if (err.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar los reportes');
            }
        }
    }

    // Manejo del estado de los datos
    useEffect(() => {
        if (!mostrarBusqueda) {
            cargarReporte();
        } else {
            busquedaReporte();
        }
        //Controla el tiempo de actualizacion de la pagina
        const interval = setInterval(() => {
            if (!mostrarBusqueda) {
                cargarReporte();
            } else {
                busquedaReporte();
            }
        }, 1200000); // 20 minutos
        return () => clearInterval(interval);

    }, [mostrarBusqueda, page]);

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // BUSQUEDA
    // Metodo de busqueda
    const busquedaReporte = async () => {
        // Verificar campos vacíos
        if (isEmptyField(nombrebuscar)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Entrada
        if (!entradaValida) {
            Swal.fire("Por favor ingrese el formato: Nombre Apellido", "", "warning");
            return;
        }
        // Flujo normal
        try {
            const datos_obtenidos_repor = await ReportesPaciente(nombrebuscar, page);
            if (datos_obtenidos_repor.data.results.length === 0) {
                setNumeropag(1);
                Swal.fire("No existen reportes con ese nombre de paciente. Ingresa un nombre válido", "", "warning");
                return;
            } else {
                setReportes(datos_obtenidos_repor.data.results);
                setNumeropag(Math.ceil(datos_obtenidos_repor.data.count / elementosPorPagina));
                setMostrarBusqueda(true);
            }
        } catch (error) {
            Swal.fire("No existen reportes con ese nombre de paciente. Ingresa un nombre válido", "", "warning");
        }
    }
    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Resetear busqueda
    const resetearBusqueda = () => {
        setMostrarBusqueda(false);
        setNombreBuscar("");
    }

    // Funcion para validar la entreada
    const cambioEntrada = (e) => {
        const value = e.target.value;
        setNombreBuscar(value);

        if (!validarEntrada(value)) {
            setEntradavaldia(false);
        } else {
            setEntradavaldia(true);
        }
    };

    // Validacion de entrada
    const validarEntrada = (value) => {
        const generar = /^[a-zA-Z]+ [a-zA-Z]+$/;
        return generar.test(value);
    };

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Reportes creadas
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
            <div className="mt-4 container" style={{ height: '50px', borderRadius: '10px' }}>
                <div className="d-flex flex-row justify-content-left w-100" style={{ alignItems: 'center', marginLeft: '1px' }}>
                    <a className="m-2" style={{ fontFamily: 'Pacifico' }}>Buscar</a>
                    <form className="d-flex flex-row justify-content-between w-50">
                        <input className="form-control mr-sm-2 w-100" type="search" name="nombre" id="nombre"
                            placeholder="Nombre del paciente.." aria-label="Search" value={nombrebuscar}
                            onChange={cambioEntrada} disabled={isTamanio} />
                        <>
                            {
                                mostrarBusqueda
                                    ? <Button variant="danger" className="my-2 my-sm-0" onClick={resetearBusqueda}>
                                        X
                                    </Button>
                                    : <Button variant="success" className="my-2 my-sm-0" onClick={busquedaReporte} disabled={isTamanio}>
                                        Ir
                                    </Button>
                            }
                        </>
                    </form>
                </div>
            </div>
            {/* Table */}
            <ListadodeReportes reportes={reportes} usuario={usuario} page={page} setPage={setPage} numeroPag={numeroPag} />
        </div>
    )

}



/* 
<div className="bg-white w-75 mt-4 container d-flex" style={{ height: '50px', borderRadius: '10px' }}>
<div className="d-flex flex-row justify-content-between w-75" style={{ alignItems: 'center', marginLeft: '10%' }}>
<a className="m-2" style={{ fontFamily: 'Pacifico' }}>Buscar</a>
*/
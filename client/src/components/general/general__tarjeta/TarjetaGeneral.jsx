// Estilos
import "../../../styles/Perfil.css"
import "../../../styles/Varios.css"
import "bootstrap/dist/css/bootstrap.min.css"
import { Card, Col, Row, Image, Button } from 'react-bootstrap';
// Componentes
import { Link, useNavigate, useParams } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash, faPencil, faBackward, faCheckCircle, faCheckDouble } from '@fortawesome/free-solid-svg-icons';
import Swal from "sweetalert2";
import { useEffect, useState } from "react";
// Metodos
import { DominioEliminar } from '../../../api/dominio.api';
import { ContenidoEliminar } from '../../../api/contenido.api';
import { IndividualEliminar, ObtenerSlugDominio, ObtenerSlugContenido } from '../../../api/contenidoindividual.api';
import { VerificarUsuario } from "../../../api/usuario.api";
//import { AtenderPeticion } from "../../../api/peticion.api"
import { ObtenerSlugCurso } from "../../../api/curso.api"
import { ReporteEliminar, ModificarEstadoResultado, CrearReporteNuevo } from "../../../api/reporte.api"


// Dominio
export function Dominio({ datos }) {
    const navigate = useNavigate();
    // Control de usuario
    const [tipoUsuario, setTipo] = useState([]);

    // Obtener tipo de usuario
    const verificacion = async () => {
        try {
            let cont = await VerificarUsuario();
            setTipo(cont.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            }
        }
    }

    // Obtener tipo de usuario
    useEffect(() => {
        verificacion();
    }, []);

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Información - Dominio
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
            <div className="mt-5 align-items-center" style={{ height: '100vh', marginLeft: '20%' }}>
                <Card className="mb-3" style={{ maxWidth: '75%' }}>
                    <Row>
                        <Col md={4}>
                            <Image
                                className="img-fluid"
                                style={{ borderRadius: '10px', height: '75%', marginTop: '20%' }}
                                src="/img/tarjeta-datos.png"
                                alt="Sample"
                                fluid
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="titulo-peticion mb-3">Dominio</Card.Title>
                                <Row className="mb-3" >
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Nombre:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datos.nombre}
                                        </Card.Text>
                                    </Col>
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Identificador</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datos.identificador_dominio}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-3">
                                    <Card.Title style={{ fontSize: '1rem' }}>Descripción:</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datos.descripcion}
                                    </Card.Text>
                                </Row>
                                <Card.Text>
                                    <small className="text-muted" style={{ fontFamily: 'Roboto' }}>Acciones</small>
                                    <div className='d-flex justify-content-between align-items-center'>
                                        <Link to={'/dominio/all'} title="Regresar" className="btn btn-primary">
                                            <FontAwesomeIcon icon={faBackward} />
                                        </Link>
                                        <>
                                            {
                                                tipoUsuario.tipo === "tecnico" ? (
                                                    <Link to={`/dominio/editar/${datos.slug_dominio}/`} title="Editar dominio"
                                                        className="btn btn-primary"><FontAwesomeIcon icon={faPencil} /></Link>
                                                ) : (
                                                    <></>
                                                )

                                            }
                                            {
                                                tipoUsuario.tipo === "tecnico" ? (
                                                    <Button title="Eliminar dominio" className="btn btn-danger"
                                                        onClick={() => {
                                                            Swal.fire({
                                                                title: '¿Está seguro que desea eliminar el dominio?',
                                                                text: "Eliminación permanente",
                                                                icon: 'warning',
                                                                showCancelButton: true,
                                                                confirmButtonColor: '#3085d6',
                                                                cancelButtonColor: '#d33',
                                                                confirmButtonText: 'Sí, eliminar',
                                                            }).then(async (result) => {
                                                                if (result.isConfirmed) {
                                                                    await DominioEliminar(datos.id);
                                                                    Swal.fire("Eliminación exitosa", "", "success");
                                                                    navigate('/dominio/all');
                                                                }
                                                            })
                                                        }}
                                                    >
                                                        <FontAwesomeIcon icon={faTrash} />
                                                    </Button>
                                                ) : (
                                                    <></>
                                                )
                                            }
                                        </>
                                    </div>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
            </div>
        </div>
    );
}

// Contenido
export function Contenido({ datos, slug }) {
    console.log(datos)
    const navigate = useNavigate();
    // Control de usuario
    const [tipoUsuario, setTipo] = useState([]);
    // Slug del dominio
    const [slugDominio, setSlugDominio] = useState("");
    const [error, setError] = useState("");

    // Obtener tipo de usuario
    const verificacion = async () => {
        try {
            let cont = await VerificarUsuario();
            setTipo(cont.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            }
        }
    }

    const cargarSlugDominio = async () => {
        try {
            const slugDomi = await ObtenerSlugDominio(slug);
            if (slugDomi.data.success) {
                setSlugDominio(slugDomi.data.slug_dominio);
            } else {
                if (slugDomi.data.success === false) {
                    navigate('/login');
                } else {
                    mostrarError(slugDomi.data.error);
                }
            }
        } catch (err) {
            if (err.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar identificador de dominio');
            }
        }
    }

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Obtener tipo de usuario
    useEffect(() => {
        verificacion();
        cargarSlugDominio();
    }, []);

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Información - Contenido
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
            {error && <span>{error}</span>}
            <div className="mt-5 align-items-center" style={{ height: '100vh', marginLeft: '20%' }}>
                <Card className="mb-3" style={{ maxWidth: '75%' }}>
                    <Row >
                        <Col md={4}>
                            <Image
                                className="img-fluid"
                                style={{ borderRadius: '10px', height: '75%', marginTop: '20%' }}
                                src="/img/tarjeta-datos.png"
                                alt="Sample"
                                fluid
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="titulo-peticion mb-4">Contenido</Card.Title>
                                <Row className="mb-3">
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Nombre :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datos.nombre}
                                        </Card.Text>
                                    </Col>
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Tipo de contenido :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datos.dominio_tipo}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-3">
                                    <Card.Title style={{ fontSize: '1rem' }}>Identificador : </Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datos.identificador_contenido}
                                    </Card.Text>
                                </Row>
                                <Card.Text>
                                    <small className="text-muted" style={{ fontFamily: 'Roboto' }}>Acciones</small>
                                    <div className='d-flex justify-content-between align-items-center'>
                                        <Link to={`/contenido/all/${slugDominio}/`} title="Regresar" className="btn btn-primary">
                                            <FontAwesomeIcon icon={faBackward} />
                                        </Link>
                                        <>
                                            {
                                                tipoUsuario.tipo === "tecnico" ? (
                                                    <Link to={`/contenido/editar/${datos.slug_contenido}/`} title="Editar contenido"
                                                        className="btn btn-primary"><FontAwesomeIcon icon={faPencil} /></Link>
                                                ) : (
                                                    <></>
                                                )
                                            }
                                            {
                                                tipoUsuario.tipo === "tecnico" ? (
                                                    <Button title="Eliminar dominio" className="btn btn-danger"
                                                        onClick={() => {
                                                            Swal.fire({
                                                                title: '¿Está seguro que desea eliminar el contenido?',
                                                                text: "Eliminación permanente",
                                                                icon: 'warning',
                                                                showCancelButton: true,
                                                                confirmButtonColor: '#3085d6',
                                                                cancelButtonColor: '#d33',
                                                                confirmButtonText: 'Sí, eliminar',
                                                            }).then(async (result) => {
                                                                if (result.isConfirmed) {
                                                                    await ContenidoEliminar(datos.id);
                                                                    Swal.fire("Eliminación exitosa", "", "success");
                                                                    navigate(`/contenido/all/${slugDominio}/`);
                                                                }
                                                            })
                                                        }}
                                                    >
                                                        <FontAwesomeIcon icon={faTrash} />
                                                    </Button>
                                                ) : (
                                                    <></>
                                                )
                                            }
                                        </>
                                    </div>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
            </div>
        </div>
    );
}


// Individual
export function Individual({ datos, slug }) {
    // Slug de contenido
    let { slug2 } = useParams();
    const navigate = useNavigate();
    /* *** Control de usuario *** */
    const [tipoUsuario, setTipo] = useState([]);
    // Slug del contenido
    const [slugContenido, setSlugContenido] = useState("");
    const [error, setError] = useState("");

    // Obtener tipo de usuario
    const verificacion = async () => {
        try {
            const cont = await VerificarUsuario();
            setTipo(cont.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            }
        }
    }

    const cargarSlugContenido = async () => {
        try {
            const slugConte = await ObtenerSlugContenido(slug);
            if (slugConte.data.success) {
                setSlugContenido(slugConte.data.slug_contenido);
            } else {
                if (slugConte.data.success === false) {
                    navigate('/login');
                } else {
                    mostrarError(slugConte.data.error);
                }
            }
        } catch (err) {
            if (err.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar identificador de dominio');
            }
        }
    }

    // Funcion para mostrar errores
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Obtener tipo de usuario
    useEffect(() => {
        verificacion();
        cargarSlugContenido();
    }, []);

    let tipoContenido;
    switch (datos.tipo_contenido) {
        case "cuento":
            tipoContenido = "Cuento";
            break;
        case "selecion_multiple":
            tipoContenido = "Selección múltiple";
            break;
        case "selecion_individual":
            tipoContenido = "Selección individual";
            break;
        case "verdadero_falso":
            tipoContenido = "Verdadero o falso";
            break;
        case "responder_preguntas":
            tipoContenido = "Responder preguntas";
            break;
        case "pintar_imagen":
            tipoContenido = "Pintar imagen";
            break;
        case "seleccionar_imagen":
            tipoContenido = "Seleccionar imagen";
            break;
        case "juego_simple":
            tipoContenido = "Juego simple";
            break;
        default:
            tipoContenido = "No definido";
            break;
    }

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Información - Actividades de estudio/entrenamiento
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
            {error && <span>{error}</span>}
            <div className="mt-5 align-items-center" style={{ height: '100vh', marginLeft: '20%' }}>
                <Card className="mb-3" style={{ maxWidth: '75%' }}>
                    <Row >
                        <Col md={4}>
                            <Image
                                className="img-fluid"
                                style={{ borderRadius: '10px', height: '60%', marginTop: '50%' }}
                                src="/img/tarjeta-datos.png"
                                alt="Sample"
                                fluid
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="titulo-peticion mb-3">Actividad</Card.Title>
                                <Row className="mb-3">
                                    <Card.Title style={{ fontSize: '1rem' }}>Descripción:</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datos.descripcion_individual}
                                    </Card.Text>
                                </Row>
                                <hr />
                                <Row className="mb-3">
                                    <Card.Title style={{ fontSize: '1rem' }}>Respuesta:</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datos.respuesta}
                                    </Card.Text>
                                </Row>
                                <hr />
                                <Row className="mb-3">
                                    <Col md={7}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Tipo contenido:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {tipoContenido}
                                        </Card.Text>
                                    </Col>
                                    <Col md={5}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Identificador:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datos.identificador_individual}
                                        </Card.Text>
                                    </Col>
                                </Row>

                                <Card.Text>
                                    <small className="text-muted" style={{ fontFamily: 'Roboto' }}>Acciones</small>
                                    <div className='d-flex justify-content-between align-items-center'>
                                        <Link to={`/contenido/individual/all/${slugContenido}/`} title="Regresar" className="btn btn-primary">
                                            <FontAwesomeIcon icon={faBackward} />
                                        </Link>
                                        <>
                                            {
                                                tipoUsuario.tipo === "tecnico" ? (
                                                    <Link to={`/individual/editar/${datos.slug_contenido_individual}/${slugContenido}/`} title="Editar contenido"
                                                        className="btn btn-primary"><FontAwesomeIcon icon={faPencil} /></Link>
                                                ) : (
                                                    <></>
                                                )
                                            }
                                            {
                                                tipoUsuario.tipo === "tecnico" ? (
                                                    <Button title="Eliminar actividad" className="btn btn-danger"
                                                        onClick={() => {
                                                            Swal.fire({
                                                                title: '¿Está seguro que desea eliminar la actividad?',
                                                                text: "Eliminación permanente",
                                                                icon: 'warning',
                                                                showCancelButton: true,
                                                                confirmButtonColor: '#3085d6',
                                                                cancelButtonColor: '#d33',
                                                                confirmButtonText: 'Sí, eliminar',
                                                            }).then(async (result) => {
                                                                if (result.isConfirmed) {
                                                                    await IndividualEliminar(datos.id);
                                                                    Swal.fire("Eliminación exitosa", "", "success");
                                                                    navigate(`/contenido/individual/all/${slugContenido}/`);
                                                                }
                                                            })
                                                        }}
                                                    >
                                                        <FontAwesomeIcon icon={faTrash} />
                                                    </Button>
                                                ) : (
                                                    <></>
                                                )
                                            }
                                        </>
                                        <Link to={`/individual/${datos.slug_contenido_individual}/${slug2}/`} className="btn btn-success"
                                            title="Ver actividad">
                                            <FontAwesomeIcon icon={faCheckCircle} />
                                        </Link>
                                    </div>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
            </div>
        </div>
    );
}


// Peticion
export function Peticion({ datos }) {
    const navigate = useNavigate();
    /* *** Control de usuario *** */
    const [tipoUsuario, setTipo] = useState([]);

    // Obtener tipo de usuario
    const verificacion = async () => {
        try {
            let cont = await VerificarUsuario();
            setTipo(cont.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            }
        }
    }

    // Obtener tipo de usuario
    useEffect(() => {
        verificacion();
    }, []);

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Peticiones
                            </h4>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-5 align-items-center" style={{ height: '100vh', marginLeft: '20%' }}>
                <Card className="mb-3" style={{ maxWidth: '75%' }}>
                    <Row >
                        <Col md={4}>
                            <Image
                                className="img-fluid img-tamaño"
                                src="/img/tarjeta-peticion.png"
                                alt="Sample"
                                fluid
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="titulo-peticion mb-3">Petición</Card.Title>
                                <Row className="mb-1">
                                    <Col md={8}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Motivo de petición:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datos.motivo_peticion}
                                        </Card.Text>
                                    </Col>
                                    <Col md={4}>
                                        <Card.Title style={{ fontSize: '1rem' }} className="text-center">Tipo:</Card.Title>
                                        <Card.Text className="texto-peticion-c">
                                            {datos.tipo_peticion}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Card.Title style={{ fontSize: '1rem' }}>Descripción:</Card.Title>
                                    <Card.Text className="texto-peticion" >
                                        {datos.peticion_cuerpo}
                                    </Card.Text>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Card.Title style={{ fontSize: '1rem' }}>Fecha de registro:</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datos.fecha_registro_peticion}
                                    </Card.Text>
                                </Row>
                                <Card.Text>
                                    <small className="text-muted" style={{ fontFamily: 'Roboto' }}>Acciones</small>
                                    <div className='d-flex justify-content-between align-items-center'>
                                        <>
                                            {
                                                tipoUsuario.tipo === "tecnico" && datos.estado_revision === false ? (
                                                    <Link to={'/peticion/all'} title="Regresar" className="btn btn-primary">
                                                        <FontAwesomeIcon icon={faBackward} />
                                                    </Link>
                                                ) : (
                                                    tipoUsuario.tipo === "comun" ? (
                                                        <Link to={'/peticion/all/usuario'} title="Regresar" className="btn btn-primary">
                                                            <FontAwesomeIcon icon={faBackward} />
                                                        </Link>
                                                    ) : (
                                                        <Link to={'/peticion/all/atendida'} title="Regresar" className="btn btn-primary">
                                                            <FontAwesomeIcon icon={faBackward} />
                                                        </Link>
                                                    )
                                                )
                                            }

                                            {
                                                tipoUsuario.tipo === "tecnico"
                                                    && datos.estado_revision === false ?
                                                    (
                                                        <Button title="Marcar revisión" className="btn btn-primary"
                                                            onClick={() => {
                                                                Swal.fire({
                                                                    title: '¿Estás seguro de marcar revisión?',
                                                                    text: "Registro de revisión",
                                                                    icon: 'warning',
                                                                    showCancelButton: true,
                                                                    confirmButtonColor: '#3085d6',
                                                                    cancelButtonColor: '#d33',
                                                                    confirmButtonText: 'Sí, enviar'
                                                                }).then((result) => {
                                                                    if (result.isConfirmed) {
                                                                        navigate(`/peticion/registro/revision/${datos.slug_peticion}/`);
                                                                    }
                                                                })
                                                            }}
                                                        >
                                                            <FontAwesomeIcon icon={faCheckCircle} />
                                                        </Button>
                                                    ) : (
                                                        <></>
                                                    )
                                            }
                                        </>
                                    </div>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
            </div>
        </div>
    );

}


// Paciente 
export function Paciente({ datosPaciente }) {
    const [slugCurso, setSlugCurso] = useState("");

    useEffect(() => {
        async function obtenerSlug() {
            try {
                let datosSlug = await ObtenerSlugCurso(datosPaciente.id);
                if (datosSlug.data.success) {
                    setSlugCurso(datosSlug.data.slug);
                } else {
                    if (datosSlug.data.message === "NOT_AUTHENTICATED") {
                        navigate('/login');
                    } else if (datosSlug.data.error) {
                        Swal.fire(datosSlug.data.error, "", "warning");
                    } else {
                        Swal.fire("No se pudo obtener el slug del curso", "", "warning");
                    }
                }
            } catch (error) {
                if (error.message === "NOT_AUTHENTICATED") {
                    navigate('/login');
                }
            }
        }
        obtenerSlug();
    }, [datosPaciente.id]);

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Información - Estudiante inscrito
                            </h4>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-5 align-items-center" style={{ height: '100vh', marginLeft: '20%' }}>
                <Card className="mb-3" style={{ maxWidth: '75%' }}>
                    <Row >
                        <Col md={4}>
                            <Image
                                className="img-fluid"
                                style={{ borderRadius: '10px', height: '60%', marginTop: '50%' }}
                                src="/img/tarjeta-paciente.png"
                                alt="Sample"
                                fluid
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="titulo-peticion">Datos del estudiante</Card.Title>
                                <Row className="mb-2">
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Nombres :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosPaciente.nombre_usuario} {datosPaciente.apellido_usuario}
                                        </Card.Text>
                                    </Col>
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Edad :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosPaciente.edad} años
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-2">
                                    <Card.Title style={{ fontSize: '1rem' }}>Correo Electrónico :</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datosPaciente.email_usuario}
                                    </Card.Text>
                                </Row>
                                <hr />
                                <Row className="mb-2" >
                                    <Col md={5}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Celular :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosPaciente.celular}
                                        </Card.Text>
                                    </Col>
                                    <Col md={7}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Cto. de Emergencia :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosPaciente.contacto_emergencia}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-2">
                                    <Card.Title style={{ fontSize: '1rem' }}>Dirección :</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datosPaciente.direccion}
                                    </Card.Text>
                                </Row>

                                <Card.Text>
                                    <small className="text-muted" style={{ fontFamily: 'Roboto' }}>Acciones</small>
                                    <div className='d-flex justify-content-between align-items-center'>
                                        <Link to={`/pacientes/all/${slugCurso}/`} title="Regresar" className="btn btn-primary">
                                            <FontAwesomeIcon icon={faBackward} />
                                        </Link>
                                    </div>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
            </div>
        </div>
    );
}

// Aplicacion
export function Aplicacion() {
    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Información Principal
                            </h4>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-5 align-items-center" style={{ height: '100vh', marginLeft: '20%' }}>
                <Card className="mb-3" style={{ maxWidth: '75%' }}>
                    <Row >
                        <Col md={4}>
                            <Image
                                className="img-fluid"
                                style={{ borderRadius: '10px', height: '60%', marginTop: '50%' }}
                                src="/img/tarjeta-paciente.png"
                                alt="Sample"
                                fluid
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="titulo-peticion">Conoce acerca de WAPIPTDAH</Card.Title>
                                <Row className="mb-2">
                                    <Card.Title style={{ fontSize: '1rem' }}>Nombres :</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        <p>
                                            Lorem, ipsum dolor sit amet consectetur adipisicing elit. Assumenda, soluta expedita inventore aut aperiam tenetur odit nam exercitationem esse saepe optio, ut consequuntur eaque sunt culpa sit dolor? Voluptatem, eius.
                                        </p>
                                    </Card.Text>
                                </Row>
                                <hr />

                                <Card.Text>
                                    <small className="text-muted" style={{ fontFamily: 'Roboto' }}>Acciones</small>
                                    <div className='d-flex justify-content-between align-items-center'>
                                        <Link to={'/nivel/all'} title="Regresar" className="btn btn-primary">
                                            <FontAwesomeIcon icon={faBackward} />
                                        </Link>
                                    </div>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
            </div>
        </div>
    );
}

// Reporte 
export function Reporte({ datosReporte }) {
    const navigate = useNavigate();
    /* *** Control de tipo de usuario *** */
    const [tipoUsuario, setTipo] = useState([]);

    // Obtener tipo de usuario
    const verificacionUser = async () => {
        try {
            let cont = await VerificarUsuario();
            setTipo(cont.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            }
        }
    }

    // Obtener tipo de usuario
    useEffect(() => {
        verificacionUser();
    }, []);

    // Control de tiempo
    const ctrTiempo = datosReporte.tiempo_m_ * 60 + datosReporte.tiempo_s_;

    // Ordenador tipo de contenido
    let contenido_tipo = "";
    // Usamos case para formatear los valores
    switch (datosReporte.tipo_contenido) {
        case "selecion_individual":
            contenido_tipo = " Selección Individual";
            break;
        case "verdadero_falso":
            contenido_tipo = "Verdadero o Falso";
            break;
        case "selecion_multiple":
            contenido_tipo = "Selección Múltiple";
            break;
        case "responder_preguntas":
            contenido_tipo = "Respuesta a preguntas";
            break;
        case "seleccionar_imagen":
            contenido_tipo = "Selección de Imágenes";
            break;
        case "cuento":
            contenido_tipo = "Lectura Comprensiva";
            break;
        case "selecion_multiple_img":
            contenido_tipo = " Selección con Imagen";
            break;
        default:
            contenido_tipo = "No definido";
            break;
    }
    
    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Reporte - WAPIPTDAH
                            </h4>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-3 align-items-center" style={{ height: '100vh', marginLeft: '10%', marginRight: '10%' }}>
                <Card className="mb-3" style={{ maxWidth: '100%' }}>
                    <div className="d-flex">
                        <div className="container d-flex justify-content-left">
                            <img src="/img/tarjeta-paciente.png" style={{ width: '6%' }} />
                            <h6 className="mt-3">
                                WAPIPTDAH - Cuidamos de nuestros niños
                            </h6>
                        </div>
                    </div>
                    <hr />
                    <div className="d-flex flex-column">
                        <div className="pt-1 pl-2 texto-reporte" >
                            Aplicación web de ayuda para niños con TDAH
                        </div>
                        <div className="pt-1 pl-2 texto-reporte">
                            Universidad Nacional de Loja
                        </div>
                        <div className="pt-1 pl-2 texto-reporte" >
                            Loja-Ecuador-La Argelia
                        </div>

                    </div>
                    <div className="d-flex flex-column fecha-reportes">
                        <div className="mt-3" style={{ fontSize: '0.8rem' }}>
                            Fecha de realización de reporte
                        </div>
                        <div className="d-flex flex-row">
                            <div class="p-2 d-flex flex-column">
                                <span>
                                    <strong style={{ fontSize: '0.8rem' }}>Fecha de inicio:</strong>
                                </span>
                                <span style={{ fontSize: '0.8rem' }}>
                                    {datosReporte.fecha_registro_reporte}
                                </span>
                            </div>
                            <div class="p-2 d-flex flex-column">
                                <span>
                                    <strong style={{ fontSize: '0.8rem' }}>Fecha de finalización</strong>
                                </span>
                                <span style={{ fontSize: '0.8rem' }}>
                                    {datosReporte.fecha_edicion_reporte}
                                </span>
                            </div>
                            <div class="p-2 d-flex flex-column">
                                <span>
                                    <strong style={{ fontSize: '0.8rem' }}>Fecha de resultado</strong>
                                </span>
                                <span style={{ fontSize: '0.8rem' }}>
                                    {datosReporte.fecha_registro_resultado_}
                                </span>
                            </div>
                            <div class="p-2 d-flex flex-column">
                                <span>
                                    <strong style={{ fontSize: '0.8rem' }}>Actividad</strong>
                                </span>
                                <span style={{ fontSize: '0.8rem' }}>
                                    {datosReporte.identificador_contenido}
                                </span>
                            </div>
                        </div>
                    </div>
                    <Row >
                        <Col md={3}>
                            <div className="d-flex flex-column">
                                <Image
                                    className="img-fluid img__descripcion"
                                    src={
                                        ctrTiempo > (40 * 60) ? "/img/alerta - rojo.jpg" :
                                            (ctrTiempo > 0 ? "/img/alerta - amarillo.png" : "")
                                    }
                                    alt="Sample"
                                    fluid
                                />
                                <div className="d-flex flex-column mt-2 w-100">
                                    <span className="texto__descripcion">
                                        Descripción de estado
                                    </span>
                                    <Card.Text className="texto-peticion tamnio_descripcion mt-2">
                                        {datosReporte.descripcion_reporte}
                                    </Card.Text>
                                    {
                                        tipoUsuario.tipo === "comun" ? (
                                            <Link to={`/editar/reporte/${datosReporte.id}/`} title="Agregar descripción"
                                                className="btn btn-success separacion--boton h mt-2">
                                                <FontAwesomeIcon icon={faPencil} />
                                            </Link>
                                        ) : <> </>
                                    }
                                </div>
                            </div>

                        </Col>
                        <Col md={9}>
                            <Card.Body>
                                <Card.Title className="titulo-peticion">Informe de estado</Card.Title>
                                <Row className="mb-1">
                                    <Col md={5}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Nombres:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosReporte.nombre_paciente} {datosReporte.apellido_paciente}
                                        </Card.Text>
                                    </Col>
                                    <Col md={3}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Edad:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosReporte.edad_paciente} años
                                        </Card.Text>
                                    </Col>
                                    <Col md={4}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Contacto:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosReporte.celular_paciente}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Col md={8}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Correo electrónico:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosReporte.correo_paciente}
                                        </Card.Text>
                                    </Col>
                                    <Col md={4}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Dirección:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosReporte.direccion_paciente}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Col md={7}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Descripción de actividad:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosReporte.descripcion_individual}
                                        </Card.Text>
                                    </Col>
                                    <Col md={5}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Tipo de contenido:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {contenido_tipo}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Col md={7}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Observación de actividad realizada:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosReporte.observacion_}
                                        </Card.Text>
                                    </Col>
                                    <Col md={5}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Respuesta ingresada:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosReporte.respuesta}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Card.Title style={{ fontSize: '1rem' }}>Tiempo de actividad realizada:</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datosReporte.tiempo_m_} minutos con {datosReporte.tiempo_s_} segundos
                                    </Card.Text>
                                </Row>
                                <hr />
                                <Card.Text>
                                    <small className="text-muted" style={{ fontFamily: 'Roboto' }}>Acciones</small>
                                    <div className='d-flex justify-content-between align-items-center'>
                                        <Link to={'/reporte/all'} title="Regresar" className="btn btn-primary">
                                            <FontAwesomeIcon icon={faBackward} />
                                        </Link>
                                        <Button title="Eliminar reporte" variant="danger" className="separacion--boton h"
                                            onClick={() => {
                                                Swal.fire({
                                                    title: '¿Está seguro que desea eliminar el reporte?',
                                                    text: "Eliminar reporte",
                                                    icon: 'warning',
                                                    showCancelButton: true,
                                                    confirmButtonColor: '#3085d6',
                                                    cancelButtonColor: '#d33',
                                                    confirmButtonText: 'Sí'
                                                }).then(async (result) => {
                                                    if (result.isConfirmed) {
                                                        const respuesta = await ModificarEstadoResultado(reporte.id);
                                                        if (respuesta.data.success) {
                                                            await ReporteEliminar(reporte.id);
                                                            Swal.fire("Eliminación exitosa", "", "success");
                                                            navigate('/reporte/all');
                                                        } else {
                                                            if (respuesta.data.error) {
                                                                Swal.fire(respuesta.data.error, '', 'error');
                                                            } else {
                                                                Swal.fire('Eliminación fallida', '', 'error');
                                                            }
                                                        }
                                                    }
                                                })
                                            }}
                                        >
                                            <FontAwesomeIcon icon={faTrash} />
                                        </Button>
                                    </div>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
            </div>
        </div>
    );
}

// Resultado
export function Resultado({ datosResultado }) {
    const navigate = useNavigate();
    /* *** Control de tipo de usuario *** */
    const [tipoUsuario, setTipo] = useState([]);

    // Obtener tipo de usuario
    const verificacionUser = async () => {
        try {
            let cont = await VerificarUsuario();
            setTipo(cont.data);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            }
        }
    }

    // Obtener tipo de usuario
    useEffect(() => {
        verificacionUser();
    }, []);

    // Ordenador tipo de contenido
    let tipoContenido = "";
    // Usamos case para formatear los valores
    switch (datosResultado.tipo_contenido) {
        case "selecion_individual":
            tipoContenido = " Selección Individual";
            break;
        case "verdadero_falso":
            tipoContenido = "Verdadero o Falso";
            break;
        case "selecion_multiple":
            tipoContenido = "Selección Múltiple";
            break;
        case "responder_preguntas":
            tipoContenido = "Respuesta a preguntas";
            break;
        case "seleccionar_imagen":
            tipoContenido = "Selección de Imágenes";
            break;
        case "cuento":
            tipoContenido = "Lectura Comprensiva";
            break;
        case "selecion_multiple_img":
            tipoContenido = " Selección con Imagen";
            break;
        default:
            tipoContenido = "No definido";
            break;
    }

    return (
        <div>
            <div className="cabeza__Nivel">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h4 className="display-7 mt-2">
                                Información - Resultado
                            </h4>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-5 align-items-center" style={{ height: '100vh', marginLeft: '10%', marginRight: '10%' }}>
                <Card className="mb-3" style={{ maxWidth: '100%' }}>
                    <Row >
                        <Col md={4}>
                            <Image
                                className="img-fluid"
                                style={{ borderRadius: '10px', height: '40%', marginTop: '90%' }}
                                src="/img/tarjeta-resultado.png"
                                alt="Sample"
                                fluid
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="titulo-peticion">Información del estudiante</Card.Title>
                                <Row className="mb-1">
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Nombres :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.nombre_paciente} {datosResultado.apellido_paciente}
                                        </Card.Text>
                                    </Col>
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Edad :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.edad_paciente} años
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Correo Electrónico :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.correo_paciente}
                                        </Card.Text>
                                    </Col>
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Celular :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.celular_paciente}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Card.Title className="titulo-peticion">Información de la actividad</Card.Title>
                                <Row className="mb-1" >
                                    <Col md={4}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Contenido :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {tipoContenido}
                                        </Card.Text>
                                    </Col>
                                    <Col md={8}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Descripción :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.descripcion_individual}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Respuesta esperada :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.respuesta}
                                        </Card.Text>
                                    </Col>
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Respuesta proporcionada :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.respuesta_contenido}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Card.Title className="titulo-peticion">Información de resultado</Card.Title>
                                <Row className="mb-1">
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Tiempo :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.tiempo_m} minutos con {datosResultado.tiempo_s} segundos
                                        </Card.Text>
                                    </Col>
                                    <Col md={6}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Fecha :</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datosResultado.fecha_registro_resultado}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-1">
                                    <Card.Title style={{ fontSize: '1rem' }}>Observación :</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        <>
                                            {
                                                datosResultado.observacion === null ? (
                                                    <Card.Text className="texto-peticion">
                                                        No se proporcionó observación
                                                    </Card.Text>
                                                ) : (
                                                    datosResultado.observacion
                                                )
                                            }
                                        </>

                                    </Card.Text>
                                </Row>
                                <Card.Text>
                                    <small className="text-muted" style={{ fontFamily: 'Roboto' }}>Acciones</small>
                                    <div className='d-flex justify-content-between align-items-center'>
                                        <Link to={'/resultado/all'} title="Regresar" className="btn btn-primary">
                                            <FontAwesomeIcon icon={faBackward} />
                                        </Link>
                                        <>
                                            {
                                                tipoUsuario.tipo === "comun" ? (
                                                    <Link to={`/resultado/editar/${datosResultado.id}`} title="Agregar observación"
                                                        className="btn btn-success separacion--boton h">
                                                        <FontAwesomeIcon icon={faPencil} />
                                                    </Link>
                                                ) : <></>
                                            }
                                            {
                                                datosResultado.estado_reporte === false && tipoUsuario.tipo === "comun" &&
                                                <Button title="Generar Reporte" variant="success"
                                                    className="separacion--boton h" disabled={datosResultado.observacion === null}
                                                    onClick={() => {
                                                        Swal.fire({
                                                            title: '¿Está seguro que desea generar el reporte?',
                                                            text: "Generar reporte",
                                                            icon: 'info',
                                                            showCancelButton: true,
                                                            confirmButtonColor: '#3085d6',
                                                            cancelButtonColor: '#d33',
                                                            confirmButtonText: 'Sí, generar'
                                                        }).then(async (result) => {
                                                            if (result.isConfirmed) {
                                                                const response = await CrearReporteNuevo(datosResultado.id);
                                                                if (response.data.success) {
                                                                    console.log(response.data);
                                                                    Swal.fire("Reporte generado de forma exitosa", "", "success");
                                                                    navigate('/reporte/all');
                                                                } else {
                                                                    if (response.data.error) {
                                                                        Swal.fire(response.data.error, '', 'error');
                                                                    } else {
                                                                        Swal.fire('Reporte fallido', '', 'error');
                                                                    }
                                                                }
                                                            }
                                                        })
                                                    }}
                                                >
                                                    <FontAwesomeIcon icon={faCheckDouble} />
                                                </Button>
                                            }
                                        </>
                                    </div>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
            </div>
        </div>
    );
}
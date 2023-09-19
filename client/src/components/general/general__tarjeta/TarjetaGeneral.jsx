// Estilos
import "../../../styles/Perfil.css"
import "bootstrap/dist/css/bootstrap.min.css"
import { Card, Col, Row, Image, Button } from 'react-bootstrap';
// Componentes
import { Link, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash, faPencil, faBackward, faCheckCircle } from '@fortawesome/free-solid-svg-icons';
import Swal from "sweetalert2";
import { useEffect, useState } from "react";
// Metodos
import { DominioEliminar } from '../../../api/dominio.api';
import { ContenidoEliminar } from '../../../api/contenido.api';
import { IndividualEliminar, ObtenerSlugDominio, ObtenerSlugContenido } from '../../../api/contenidoindividual.api';
import { VerificarUsuario } from "../../../api/usuario.api";
//import { AtenderPeticion } from "../../../api/peticion.api"
import { ObtenerSlugCurso } from "../../../api/curso.api"

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
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar identificador de dominio');
            }
        }
    }

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
                                                                    navigate('/contenido/all');
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
    const navigate = useNavigate();
    /* *** Control de usuario *** */
    const [tipoUsuario, setTipo] = useState([]);
    // Slug del contenido
    const [slugContenido, setSlugContenido] = useState("");

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
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al cargar identificador de dominio');
            }
        }
    }

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
                                                    <Link to={`/individual/editar/${datos.slug_contenido_individual}/`} title="Editar contenido"
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
                                                                    navigate('/contenido/individual/all');
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
                                <Row className="mb-3">
                                    <Col md={8}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Motivo de petición:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datos.motivo_peticion}
                                        </Card.Text>
                                    </Col>
                                    <Col md={4}>
                                        <Card.Title style={{ fontSize: '1rem' }}>Tipo:</Card.Title>
                                        <Card.Text className="texto-peticion">
                                            {datos.tipo_peticion}
                                        </Card.Text>
                                    </Col>
                                </Row>
                                <hr />
                                <Row className="mb-3">
                                    <Card.Title style={{ fontSize: '1rem' }}>Descripción:</Card.Title>
                                    <Card.Text className="texto-peticion">
                                        {datos.peticion_cuerpo}
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
                                Información - Paciente inscrito
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
                                <Card.Title className="titulo-peticion">Datos del paciente</Card.Title>
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
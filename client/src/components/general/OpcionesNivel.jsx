// Estilos
//import "../../styles/Nivel.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from 'react-bootstrap';
// Componentes
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom";
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faPencil, faTrashCan } from '@fortawesome/free-solid-svg-icons';
// Metodos
import { NivelEliminar } from "../../api/grado.api";


export function OpcionesTecnico({ nivel }) {
    return (
        <div className="contenedor-opciones__nivel d-flex flex-column justify-content-between">
            <ul>
                <li>
                    <h3 className="titulo__dato"> Opciones </h3>
                </li>
                <div className="LL d-flex flex-row justify-content-between">
                    <li>
                        <Link to={`/nivel/editar/${nivel.slug_grado}/`} className="btn btn-primary"
                            title="Editar nivel"><FontAwesomeIcon icon={faPencil} /></Link>
                    </li>
                    <li>
                        <Button title="Eliminar nivel" className="btn btn-danger"
                            onClick={() => {
                                Swal.fire({
                                    title: '¿Está seguro que desea eliminar el nivel?',
                                    text: "Eliminación permanente",
                                    icon: 'warning',
                                    showCancelButton: true,
                                    confirmButtonColor: '#3085d6',
                                    cancelButtonColor: '#d33',
                                    confirmButtonText: 'Sí, eliminar',
                                }).then(async (result) => {
                                    if (result.isConfirmed) {
                                        await NivelEliminar(nivel.id);
                                        Swal.fire("Eliminación exitosa", "", "success");
                                        navigate('/nivel/all');
                                    }
                                })
                            }}
                        >
                            <FontAwesomeIcon icon={faTrashCan} />
                        </Button>
                    </li>
                    <li>
                        <Link to={'/dominio/all'} className="btn btn-primary"
                            title="Ver detalle"><FontAwesomeIcon icon={faEye} /></Link>
                    </li>
                </div>
            </ul>
        </div>
    )
}

export function OpcionesComun({ nivel }) {
    const navigate = useNavigate();
    return (
        <div className="contenedor-opciones__nivel d-flex flex-column justify-content-between">
            <ul>
                <li>
                    <h3 className="titulo__dato"> Opciones </h3>
                </li>
                <div className="LL d-flex flex-row justify-content-between">
                    <li>
                        <Button title="Solicitar edición de nivel" className="btn btn-primary"
                            onClick={() => {
                                Swal.fire({
                                    title: '¿Estás seguro?',
                                    text: "Registrar una petición para nivel",
                                    icon: 'warning',
                                    showCancelButton: true,
                                    confirmButtonColor: '#3085d6',
                                    cancelButtonColor: '#d33',
                                    confirmButtonText: 'Sí, enviar'
                                }).then((result) => {
                                    if (result.isConfirmed) {
                                        navigate('/peticion/registro');
                                    }
                                })
                            }}
                        >
                            <FontAwesomeIcon icon={faPencil} />
                        </Button>
                    </li>
                    <li>
                        <Link to={'/dominio/all'} className="btn btn-primary"
                            title="Ver detalle"><FontAwesomeIcon icon={faEye} /></Link>
                    </li>
                </div>
            </ul>
        </div>
    )
}

export function OpcionesPaciente({ nivel }) {
    return (
        <div className="contenedor-opciones__nivel d-flex flex-column justify-content-between h-100">
            <ul>
                <li>
                    <h3 className="titulo__dato"> Opciones </h3>
                </li>
                <div className="opciones-paciente d-flex justify-content-center">
                    <li >
                        <Link to={'/dominio/all'} className="btn btn-primary"
                            title="Ver detalle"><FontAwesomeIcon icon={faEye} /></Link>
                    </li>
                </div>
            </ul>
        </div>
    )
}
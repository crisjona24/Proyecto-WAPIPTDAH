// Estilos
import "../../styles/Lista.css"
import "bootstrap/dist/css/bootstrap.min.css";
import { Button, Table } from "react-bootstrap";
// Componentes
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBackward, faCheckDouble, faPencil, faTrash, faPlusCircle, faEye } from '@fortawesome/free-solid-svg-icons';
import { Link, useNavigate } from 'react-router-dom';
//import { useState } from "react";
import React from 'react';
import Swal from "sweetalert2";
// Metodos
import { SalaEliminar, AtenderSala } from "../../api/sala.api"
import { ReporteEliminar, CrearReporteNuevo, ModificarEstadoResultado } from "../../api/reporte.api"
import { ResultadoEliminar } from "../../api/resultado.api"


// Sala generales
export function ListadodeSala({ salas, usuario, page, setPage, numeroPag }) {
    const navigate = useNavigate();
    // Paginacion siguente
    const anterior = () => {
        setPage(prevPage => (prevPage > 1 ? prevPage - 1 : prevPage));
    };
    // Paginacion anterior
    const siguiente = () => {
        setPage(prevPage => (prevPage < numeroPag ? prevPage + 1 : prevPage));
    };

    return (
        <div className="cuerpo-tabla-2">
            <div className="row">
                <div className="col-md-offset-1 col-md-11">
                    <div className="panel">
                        <div className="panel-heading">
                            <div className="row">
                                <div className="col-sm-12 col-xs-12">
                                    <>
                                        {
                                            usuario.tipo === "comun" &&
                                            <Link to={'/sala/registro'} className="btn btn-sm btn-primary pull-left">
                                                <FontAwesomeIcon icon={faPlusCircle} title="Agregar sala" /> Agregar nuevo
                                            </Link>
                                        }
                                    </>
                                </div>
                            </div>
                        </div>
                        <div className="panel-body_2 table-responsive">
                            <Table responsive="sm" className="table">
                                <thead>
                                    <tr>

                                        <th>Nombre</th>
                                        <th className="text-center">Código</th>
                                        <th>Anotaciones</th>
                                        <th className="text-center">Fecha</th>
                                        <th className="text-center">Opciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <>
                                        {
                                            salas.map((sala) => (
                                                <tr key={sala.id}>
                                                    <td>{sala.nombre_sala}</td>
                                                    <td className="text-center">{sala.codigo_identificador}</td>
                                                    <td style={{ textAlign: 'justify' }}>{sala.anotaciones}</td>
                                                    <td className="text-center">{sala.fecha_registro_sala}</td>
                                                    <td >
                                                        <ul
                                                            className={`action-list ${sala.sala_atendida === true && usuario.tipo === 'comun' ? 'd-flex justify-content-center'
                                                                : usuario.tipo === 'tecnico' ? 'd-flex justify-content-center' :
                                                                    sala.sala_atendida == false && usuario.tipo === 'comun' ? 'd-flex justify-content-center'
                                                                        : ""}`}>
                                                            <Button title="Eliminar sala" variant="danger"
                                                                className="separacion--boton h"
                                                                onClick={() => {
                                                                    Swal.fire({
                                                                        title: '¿Está seguro que desea eliminar la sala?',
                                                                        text: "Eliminar sala creada",
                                                                        icon: 'warning',
                                                                        showCancelButton: true,
                                                                        confirmButtonColor: '#3085d6',
                                                                        cancelButtonColor: '#d33',
                                                                        confirmButtonText: 'Sí'
                                                                    }).then(async (result) => {
                                                                        if (result.isConfirmed) {
                                                                            await SalaEliminar(sala.id);
                                                                            Swal.fire("Eliminación exitosa", "", "success");
                                                                            navigate('/nivel/all');
                                                                        }
                                                                    })
                                                                }}
                                                            >
                                                                <FontAwesomeIcon icon={faTrash} />
                                                            </Button>
                                                            {
                                                                usuario.tipo === "comun" && sala.sala_atendida === false &&
                                                                <Link to={`/sala/editar/${sala.id}/`} title="Editar sala"
                                                                    className="btn btn-primary separacion--boton h">
                                                                    <FontAwesomeIcon icon={faPencil} />
                                                                </Link>
                                                            }
                                                        </ul>
                                                    </td>
                                                </tr>
                                            ))
                                        }
                                        {
                                            salas.length === 0 &&
                                            <tr >
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td>
                                                    <ul></ul>
                                                </td>
                                            </tr>
                                        }
                                    </>
                                </tbody>
                            </Table>
                        </div>
                        <div className="panel-footer">
                            <div className="row">
                                <div className="col-sm-1 col-xs-1">
                                    <Link to={'/nivel/all'} className="btn btn-primary" title="Atrás">
                                        <FontAwesomeIcon icon={faBackward} />
                                    </Link>
                                </div>
                                <div className="col-sm-7 col-xs-7">Información - Salas Creadas</div>
                                <div className="pagination-controls col-sm-4 col-xs-4">
                                    <Button onClick={anterior} disabled={page === 1}
                                        className="separacion--boton" title="Atrás">
                                        <FontAwesomeIcon icon={faBackward} />
                                    </Button>
                                    <span style={{ fontSize: '0.8rem' }}>Página {page} de {numeroPag}</span>
                                    <Button onClick={siguiente} disabled={page === numeroPag}
                                        className="separacion--boton--derecha" title="Adelante">
                                        <FontAwesomeIcon icon={faBackward} style={{ transform: 'rotate(180deg)' }} />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}


// Sala de paciente
export function ListadodeSalaPaciente({ salas, page, setPage, numeroPag }) {
    // Paginacion siguente
    const anterior = () => {
        setPage(prevPage => (prevPage > 1 ? prevPage - 1 : prevPage));
    };
    // Paginacion anterior
    const siguiente = () => {
        setPage(prevPage => (prevPage < numeroPag ? prevPage + 1 : prevPage));
    };

    return (
        <div className="cuerpo-tabla-3">
            <div className="row">
                <div className="col-md-offset-1 col-md-11">
                    <div className="panel">
                        <div className="panel-heading">
                            <div className="row">
                            </div>
                        </div>
                        <div className="panel-body_3 table-responsive">
                            <Table responsive="sm" className="table">
                                <thead>
                                    <tr>

                                        <th>Nombre</th>
                                        <th>Código</th>
                                        <th>Anotaciones</th>
                                        <th className="text-center">Fecha</th>
                                        <th className="text-center">Opciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <>
                                        {
                                            salas.map((sala) => (
                                                <tr key={sala.id}>
                                                    <td>{sala.nombre_sala}</td>
                                                    <td>{sala.codigo_identificador}</td>
                                                    <td style={{ textAlign: 'justify' }}>{sala.anotaciones}</td>
                                                    <td className="text-center">{sala.fecha_registro_sala}</td>
                                                    <td>
                                                        <ul className="action-list d-flex justify-content-center" >
                                                            <Button title="Atender sala" variant="success" className="separacion--boton h"
                                                                onClick={() => {
                                                                    Swal.fire({
                                                                        title: '¿La sala ha sido atendida?',
                                                                        text: "Atender sala",
                                                                        icon: 'info',
                                                                        showCancelButton: true,
                                                                        confirmButtonColor: '#3085d6',
                                                                        cancelButtonColor: '#d33',
                                                                        confirmButtonText: 'Sí'
                                                                    }).then(async (result) => {
                                                                        if (result.isConfirmed) {
                                                                            try {
                                                                                const response = await AtenderSala(sala.slug_sala);
                                                                                if (response.data.success) {
                                                                                    Swal.fire("Atención exitosa", "", "success");
                                                                                    window.location.reload();
                                                                                } else {
                                                                                    if (response.data.error) {
                                                                                        Swal.fire(response.data.error, '', 'error');
                                                                                    } else {
                                                                                        Swal.fire('Atención fallida', '', 'error');
                                                                                    }
                                                                                }
                                                                            } catch (error) {
                                                                                Swal.fire("Atención fallida", "", "error");
                                                                            }
                                                                        }
                                                                    })
                                                                }}
                                                            >
                                                                <FontAwesomeIcon icon={faCheckDouble} />
                                                            </Button>
                                                        </ul>
                                                    </td>
                                                </tr>
                                            ))
                                        }
                                        {
                                            salas.length === 0 &&
                                            <tr >
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td>
                                                    <ul></ul>
                                                </td>
                                            </tr>
                                        }
                                    </>
                                </tbody>
                            </Table>
                        </div>
                        <div className="panel-footer">
                            <div className="row">
                                <div className="col-sm-1 col-xs-1">
                                    <Link to={'/nivel/all'} className="btn btn-primary" title="Atrás">
                                        <FontAwesomeIcon icon={faBackward} />
                                    </Link>
                                </div>
                                <div className="col-sm-7 col-xs-7">Información - Salas</div>
                                <div className="pagination-controls col-sm-4 col-xs-4">
                                    <Button onClick={anterior} disabled={page === 1}
                                        className="separacion--boton" title="Atrás">
                                        <FontAwesomeIcon icon={faBackward} />
                                    </Button>
                                    <span style={{ fontSize: '0.8rem' }}>Página {page} de {numeroPag}</span>
                                    <Button onClick={siguiente} disabled={page === numeroPag}
                                        className="separacion--boton--derecha" title="Adelante">
                                        <FontAwesomeIcon icon={faBackward} style={{ transform: 'rotate(180deg)' }} />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}


// Lista de resultados
export function ListadodeResultado({ resultados, usuario, page, setPage, numeroPag }) {
    const navigate = useNavigate();
    // Paginacion siguente
    const anterior = () => {
        setPage(prevPage => (prevPage > 1 ? prevPage - 1 : prevPage));
    };
    // Paginacion anterior
    const siguiente = () => {
        setPage(prevPage => (prevPage < numeroPag ? prevPage + 1 : prevPage));
    };

    return (
        <div className="cuerpo-tabla-2">
            <div className="row">
                <div className="col-md-offset-1 col-md-11">
                    <div className="panel">
                        <div className="panel-heading">
                            <div className="row">
                            </div>
                        </div>
                        <div className="panel-body_2 table-responsive">
                            <Table responsive="sm" className="table">
                                <thead>
                                    <tr>

                                        <th>Paciente</th>
                                        <th>Tiempo</th>
                                        <th>Observación</th>
                                        <th style={{ textAlign: 'center' }}>Fecha</th>
                                        <th style={{ textAlign: 'center' }}>Opciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <>
                                        {
                                            resultados.map((resultado) => (
                                                <tr key={resultado.id}>
                                                    <td>{resultado.nombre_paciente} {resultado.apellido_paciente}</td>
                                                    <td>{resultado.tiempo_m} m {resultado.tiempo_s} s</td>
                                                    <>
                                                        {
                                                            resultado.observacion === null ?
                                                                <td>No hay observación. !Agrégala¡</td>
                                                                :
                                                                <td style={{ textAlign: 'justify' }}>{resultado.observacion}</td>
                                                        }

                                                    </>
                                                    <td style={{ textAlign: 'center' }}>{resultado.fecha_registro_resultado}</td>
                                                    <td>
                                                        <ul className="action-list d-flex justify-content-center">
                                                            <>
                                                                {
                                                                    resultado.estado_reporte === false && usuario.tipo === "comun" &&
                                                                    <Button title="Generar Reporte" variant="success"
                                                                        className="separacion--boton h" disabled={resultado.observacion === null}
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
                                                                                    const response = await CrearReporteNuevo(resultado.id);
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
                                                            <Button title="Eliminar resultado" variant="danger" className="separacion--boton h"
                                                                onClick={() => {
                                                                    Swal.fire({
                                                                        title: '¿Está seguro que desea eliminar el resultado?',
                                                                        text: "Eliminar resultado",
                                                                        icon: 'warning',
                                                                        showCancelButton: true,
                                                                        confirmButtonColor: '#3085d6',
                                                                        cancelButtonColor: '#d33',
                                                                        confirmButtonText: 'Sí'
                                                                    }).then(async (result) => {
                                                                        if (result.isConfirmed) {
                                                                            await ResultadoEliminar(resultado.id);
                                                                            Swal.fire("Eliminación exitosa", "", "success");
                                                                            navigate('/resultado/all');
                                                                        }
                                                                    })
                                                                }}
                                                            >
                                                                <FontAwesomeIcon icon={faTrash} />
                                                            </Button>
                                                            {
                                                                usuario.tipo === "comun" &&
                                                                <Link to={`/resultado/editar/${resultado.id}`} title="Agregar observación"
                                                                    className="btn btn-primary separacion--boton h">
                                                                    <FontAwesomeIcon icon={faPencil} />
                                                                </Link>
                                                            }
                                                            {
                                                                usuario.tipo === "comun" &&
                                                                <Link to={`/ver/resultados/${resultado.id}`} title="Ver descripción"
                                                                    className="btn btn-success separacion--boton h">
                                                                    <FontAwesomeIcon icon={faEye} />
                                                                </Link>
                                                            }
                                                        </ul>
                                                    </td>
                                                </tr>
                                            ))
                                        }
                                        {
                                            resultados.length === 0 &&
                                            <tr >
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td>
                                                    <ul></ul>
                                                </td>
                                            </tr>
                                        }
                                    </>
                                </tbody>
                            </Table>
                        </div>
                        <div className="panel-footer">
                            <div className="row">
                                <div className="col-sm-1 col-xs-1">
                                    <Link to={'/nivel/all'} className="btn btn-primary" title="Atrás">
                                        <FontAwesomeIcon icon={faBackward} />
                                    </Link>
                                </div>
                                <div className="col-sm-7 col-xs-7">Información - Resultados</div>
                                <div className="pagination-controls col-sm-4 col-xs-4">
                                    <Button onClick={anterior} disabled={page === 1}
                                        className="separacion--boton" title="Atrás">
                                        <FontAwesomeIcon icon={faBackward} />
                                    </Button>
                                    <span style={{ fontSize: '0.8rem' }}>Página {page} de {numeroPag}</span>
                                    <Button onClick={siguiente} disabled={page === numeroPag}
                                        className="separacion--boton--derecha" title="Adelante">
                                        <FontAwesomeIcon icon={faBackward} style={{ transform: 'rotate(180deg)' }} />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}


// Listado de reportes
export function ListadodeReportes({ reportes, usuario, page, setPage, numeroPag }) {
    const navigate = useNavigate();
    // Paginacion siguente
    const anterior = () => {
        setPage(prevPage => (prevPage > 1 ? prevPage - 1 : prevPage));
    };
    // Paginacion anterior
    const siguiente = () => {
        setPage(prevPage => (prevPage < numeroPag ? prevPage + 1 : prevPage));
    };

    return (
        <div className="cuerpo-tabla">
            <div className="row">
                <div className="col-md-offset-1 col-md-11">
                    <div className="panel">
                        <div className="panel-heading">
                            <div className="row">
                            </div>
                        </div>
                        <div className="panel-body_3 table-responsive">
                            <Table responsive="sm" className="table">
                                <thead>
                                    <tr>

                                        <th>Paciente</th>
                                        <th >Tiempo</th>
                                        <th>Correo</th>
                                        <th className="text-center">Fecha</th>
                                        <th class="text-center">Opciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <>
                                        {
                                            reportes.map((reporte) => (
                                                <tr key={reporte.id}>
                                                    <td>{reporte.nombre_paciente} {reporte.apellido_paciente}</td>
                                                    <td>{reporte.tiempo_m_} m con {reporte.tiempo_s_} s</td>
                                                    <td>{reporte.correo_paciente}</td>
                                                    <td className="text-center">{reporte.fecha_registro_reporte}</td>
                                                    <td>
                                                        <ul className="action-list d-flex justify-content-center">
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
                                                                                window.location.reload();
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
                                                            <Link to={`/ver/reporte/${reporte.id}/`} title="Ver reporte"
                                                                className="btn btn-primary separacion--boton h">
                                                                <FontAwesomeIcon icon={faEye} />
                                                            </Link>
                                                        </ul>
                                                    </td>
                                                </tr>
                                            ))
                                        }
                                        {
                                            reportes.length === 0 &&
                                            <tr >
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td>
                                                    <ul></ul>
                                                </td>
                                            </tr>
                                        }
                                    </>
                                </tbody>
                            </Table>
                        </div>
                        <div className="panel-footer">
                            <div className="row">
                                <div className="col-sm-1 col-xs-1">
                                    <Link to={'/nivel/all'} className="btn btn-primary" title="Atrás">
                                        <FontAwesomeIcon icon={faBackward} />
                                    </Link>
                                </div>
                                <div className="col-sm-7 col-xs-7">Información - Reportes Creados</div>
                                <div className="pagination-controls col-sm-4 col-xs-4">
                                    <Button onClick={anterior} disabled={page === 1}
                                        className="separacion--boton" title="Atrás">
                                        <FontAwesomeIcon icon={faBackward} />
                                    </Button>
                                    <span style={{ fontSize: '0.8rem' }}>Página {page} de {numeroPag}</span>
                                    <Button onClick={siguiente} disabled={page === numeroPag}
                                        className="separacion--boton--derecha" title="Adelante">
                                        <FontAwesomeIcon icon={faBackward} style={{ transform: 'rotate(180deg)' }} />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}
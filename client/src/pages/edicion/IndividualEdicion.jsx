// Objetivo: Edición de contenido
// Estilos
import "bootstrap/dist/css/bootstrap.min.css"
import { Button, Modal, Container, Row } from "react-bootstrap";
// Componentes
import { CabeceraRegister } from '../../components/partes/CabecerRegister'
import { PieRegister } from '../../components/partes/PieRegister'
import { Link } from 'react-router-dom';
import React, { useState } from 'react';
// Metodos
import { FormularioEdicionIndividual } from '../../components/edicion/Formularo_edicion'

export function IndividualEdición() {
    const [show, setShow] = useState(false);
    const cerrar = () => setShow(false);
    const abrir = () => setShow(true);

    return (
        <div style={{ width: '100%', height: '100%' }}>
            {/* MODAL */}
            <>
                <Modal show={show} onHide={cerrar} centered>
                    <Modal.Header closeButton>
                        <Modal.Title>Indicaciones</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <h6>Sección: Indicación</h6>
                        <p style={{ color: '#333', textAlign: 'justify', fontSize: '1rem' }}>
                            Ingresa la indicación para la actividad. Si son preguntas multiples
                            previo a una pregunta usa ',' para separarlas.
                            Ejm: Responda, ¿P1?, ¿P2?
                        </p>
                        <h6>Sección: Respuesta</h6>
                        <p style={{ color: '#333', textAlign: 'justify', fontSize: '1rem' }}>
                            Ingresa las respuestas para la actividad. Si son respuestas multiples
                            previo a una usa ',' para separarlas.
                        </p>
                        <h6>Sección: Portada</h6>
                        <p style={{ color: '#333', textAlign: 'justify', fontSize: '1rem' }}>
                            Se debe elegir una imagen con el nombre plasmado en ella.
                            Imagina que es un rotulador en ella que representa el nombre
                            del Contenido.</p>
                        <h6>Sección: Contenido</h6>
                        <p style={{ color: '#333', textAlign: 'justify', fontSize: '1rem' }}>
                            Se debe elegir una imagen que representa la actividad a resolver
                            según la indicación plasmada.</p>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="success" onClick={cerrar}>
                            Entendido
                        </Button>
                    </Modal.Footer>
                </Modal>
            </>
            {/* FIN MODAL */}
            <CabeceraRegister />
            <Container className='mb-5' style={{ width: '35%' }}>
                <Container className='barraSup mt-5' >
                    <Row className='col-md-12'>
                        <div className="card-body col-md-7">
                            <h4 style={{ padding: '10px', fontSize: '1.4rem' }}> Edición de contenido</h4>
                        </div>
                        <div className='card-body col-md-2'>
                            <Button variant="success" onClick={abrir} className='mt-2'>
                                Detalle
                            </Button>
                        </div>
                        <div className='card-body col-md-2'>
                            <Link to={'/contenido/individual/all'} className='btn btn-danger mt-2'>
                                Cancelar
                            </Link>
                        </div>
                    </Row>
                </Container>
                <Container className='form container pb-1' style={{ border: '1px solid #333' }}>
                    <h6 className='pl-0 pt-3 pb-3'> Ingrese los datos solicitados</h6>
                    <div className='pb-2'>
                        <FormularioEdicionIndividual />
                    </div>
                </Container>
            </Container>
            <PieRegister />
        </div>
    )
}
// Estilos
import "bootstrap/dist/css/bootstrap.min.css";
import {Container, Row} from "react-bootstrap";
// Componentes
import { CabeceraRegister } from '../../components/partes/CabecerRegister';
import { PieRegister } from '../../components/partes/PieRegister';
import { Link } from 'react-router-dom';
// Metodos
import { FormularioEdicionCurso } from "../../components/edicion/Formularo_edicion";

export function CursoEdicion() {
    return (
        <div style={{ width: '100%', height: '100%' }}>
            <CabeceraRegister />
            <Container className='mb-5' style={{ width: '35%' }}>
                <Container className='barraSup mt-5' >
                    <Row className='col-md-12'>
                        <div className="card-body col-md-9">
                            <h4 style={{ padding: '10px', fontSize: '1.5rem', paddingTop: '15px' }}> Edición de Curso</h4>
                        </div>
                        <div className='card-body col-md-2 pt-1'>
                            <Link to={'/cursos/all'} className='btn btn-danger mt-2'>
                                Cancelar
                            </Link>
                        </div>
                    </Row>
                </Container>
                <Container className='form container pb-1' style={{ border: '1px solid #333' }}>
                    <h6 className='pl-0 pt-3 pb-3'> Ingrese los datos solicitados</h6>
                    <div className='pb-2'>
                        {/* Formulario */}
                        <FormularioEdicionCurso />
                    </div>
                </Container>
            </Container>
            <PieRegister />
        </div>
    )
}
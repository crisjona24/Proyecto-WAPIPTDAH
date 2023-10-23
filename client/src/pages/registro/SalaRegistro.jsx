// Estilos
import "bootstrap/dist/css/bootstrap.min.css";
import { Row, Container } from "react-bootstrap"
// Componentes
import { CabeceraRegister } from '../../components/partes/CabecerRegister';
import { PieRegister } from '../../components/partes/PieRegister'
import { Link } from 'react-router-dom';
// Metodos
import { FormularioSala, FormularioPeticionRevision } from "../../components/registro/Formularios"

export function SalaRegistro() {
    return (
        <div style={{ width: '100%', height: '100%' }}>
            <CabeceraRegister />
            <Container className="contenedor__edicion">
                <Container className='barraSup mt-5' >
                    <Row className='col-md-12'>
                        <div className="card-body col-md-9">
                            <h4 className="titulo__CE"> Registro de Sala</h4>
                        </div>
                        <div className='card-body col-md-2 pt-1'>
                            <Link to={'/sala/all'} className='btn btn-danger mt-2'>
                                Cancelar
                            </Link>
                        </div>
                    </Row>
                </Container>
                <Container className='form container pb-1 borde__CE'>
                    <h6 className='pl-0 pt-3 pb-3'> Ingrese los datos solicitados</h6>
                    <div className='pb-2'>
                        {/* Formulario */}
                        <FormularioSala />
                    </div>
                </Container>
            </Container>
            <PieRegister />
        </div>
    )
}

export function RevisionPeticionRegistro() {
    return (
        <div style={{ width: '100%', height: '100%' }}>
            <CabeceraRegister />
            <Container className='mb-5' style={{ width: '40%' }}>
                <Container className='barraSup mt-5' >
                    <Row className='col-md-12'>
                        <div className="card-body col-md-10">
                            <h4 className="titulo__CE"> Registro de Revisión</h4>
                        </div>
                        <div className='card-body col-md-2 pt-1'>
                            <Link to={'/peticion/all'} className='btn btn-danger mt-2'>
                                Cancelar
                            </Link>
                        </div>
                    </Row>
                </Container>
                <Container className='form container pb-1 borde__CE'>
                    <h6 className='pl-0 pt-3 pb-3'> Ingrese los datos solicitados</h6>
                    <div className='pb-2'>
                        {/* Formulario */}
                        <FormularioPeticionRevision />
                    </div>
                </Container>
            </Container>
            <PieRegister />
        </div>
    )
}
// Estilos
import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "react-bootstrap";
// Componentes
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Swal from "sweetalert2";
// Metodos
import { info__nivel, info__dominio } from '../../controles/controlador_registro';
import { CrearCurso } from '../../api/curso.api';
import { VerificarCuenta } from '../../api/usuario.api';
import { CrearNivelNew } from '../../api/grado.api';
import { CrearPeticion, AtenderPeticion } from '../../api/peticion.api';
import { validarTamanoImagen } from '../../controles/alert_user';
import { CrearDominioNew } from '../../api/dominio.api';
import { CrearContenidoNew } from '../../api/contenido.api'
import { DominiosListadoSolo } from '../../api/dominio.api'
import { CrearSalaNueva } from '../../api/sala.api'

/* SELECCION DE ACTIVIDAD */
export function Actividad() {
    /* *** Form **** */
    const [actividad, setActividad] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!isValidForm()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            if (actividad === "Tecnico") {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                navigate('/usuario/registro');
            } else if (actividad === "Paciente") {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                navigate('/usuario/paciente/registro');
            } else if (actividad === "Comun") {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                navigate('/usuario/comun/registro');
            }
            else {
                mostrarError('Error al seleccionar actividad');
            }
        } catch (err) {
            mostrarError('Error al seleccionar actividad');
        }
    };

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Validar espacios
    const isValidForm = () => {
        if (
            actividad.trim() === ""
        ) {
            return false;
        }
        return true;
    }

    return (
        <form onSubmit={handleSubmit}>
            {error && <span>{error}</span>}
            <div className="form-group">
                <label className='label' htmlFor="actividad">Selecciona su actividad:</label>
                <select className="form-control w-100" id="actividad"
                    name="actividad" value={actividad} onChange={e => setActividad(e.target.value)}>
                    <option value="none">----</option>
                    <option value="Tecnico">Técnico</option>
                    <option value="Paciente">Paciente</option>
                    <option value="Comun">Común</option>
                </select>
            </div>
            <button type='submit' className='btn btn-success'>Seleccionar</button>
        </form>
    )
}


/* FORMULARIO CONTENIDO */
export function FormularioContenido({ slug }) {
    /* *** Form **** */
    const [nombre, setNombre] = useState("");
    const [dominio_tipo, setDominio] = useState("");
    const [portada, setPortada] = useState("");
    const [dominios, setDominios] = useState([]);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const enviar = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!isValidForm()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        //Flujo normal
        try {
            const formData = new FormData(); // Crear un objeto FormData
            formData.append('nombre', nombre);
            formData.append('dominio_tipo', dominio_tipo);
            formData.append('portada', portada);
            // Guardar
            await guardar(formData);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar contenido');
            }
        }
    };

    // Funcion para guardar datos
    const guardar = async (formData) => {
        try {
            // Realizar la petición POST al servidor
            const response = await CrearContenidoNew(formData);
            if (response.data.success) {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                navigate(`/contenido/all/${slug}/`);
            } else {
                if (response.data.error) {
                    Swal.fire(response.data.error, '', 'error')
                } else {
                    mostrarError('Error al registrar contenido');
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar contenido');
            }
        }
    }

    // Obtener dominios
    useEffect(() => {
        async function cargarDominios() {
            try {
                const data = await DominiosListadoSolo();
                setDominios(data.data);
            } catch (error) {
                setError('Error al obtener datos de dominio', error);
                setTimeout(() => {
                    setError(""); // Esto limpiará el mensaje de error después de 5 segundos
                }, 5000);
            }
        };
        cargarDominios();
    }, []);

    // Campos vacios
    const isValidForm = () => {
        if (
            nombre.trim() === "" ||
            dominio_tipo.trim() === "" ||
            !portada
        ) {
            return false;
        }
        return true;
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <form onSubmit={enviar} encType='multipart/form-data'>
            <>
                {error && <p>{error}</p>}
            </>
            <div className="form-group">
                <label className='label' htmlFor="nombre">Nombre de contenido:</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese el nombre**" id="nombre"
                    value={nombre} onChange={e => setNombre(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="dominio">Tipo de contenido:</label>
                <select className="form-control w-100" id="dominio"
                    name="dominio" value={dominio_tipo} onChange={e => setDominio(e.target.value)}>
                    <option value="none">None</option>
                    <>
                        {dominios.map((dominio) => (
                            <option key={dominio.id} value={dominio.nombre}>
                                {dominio.nombre}
                            </option>
                        ))}
                    </>
                </select>
            </div>
            <div className="form-group">
                <label className='label' htmlFor="portada_contenido">Portada:</label>
                <input className='form-control w-100' type="file" id="portada_contenido"
                    onChange={e => { setPortada(e.target.files[0]); validarTamanoImagen(e.target) }}
                    name='portada_contenido' accept="image/*" />
            </div>
            <Button type='submit' className='btn btn-success' >
                Guardar
            </Button>
        </form>
    )
}


/* FORMULARIO DE CURSO */
export function FormularioCurso() {
    /* *** Form **** */
    const [nombre_curso, setNombreCurso] = useState("");
    const [descripcion, setDescripcionCurso] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Operacion de guardado
    const enviarFC = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (isEmptyField(nombre_curso, descripcion)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            // Obtenemos los datos
            const datos__post = {
                nombre_curso,
                descripcion
            };
            // Realizar la petición POST al servidor
            await guardar(datos__post);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar curso');
            }
        }
    };

    // Funcion para guardar
    const guardar = async (datos__post) => {
        try {
            const response = await CrearCurso(datos__post);
            if (response.data.success) {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                Swal.fire("Curso registrado correctamente", "", "success");
                navigate('/cursos/all');
            } else {
                if (response.data.error) {
                    Swal.fire(response.data.error, '', 'error')
                } else {
                    mostrarError('Error al registrar curso');
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar curso');
            }
        }
    }

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <form onSubmit={enviarFC}>
            {error && <span>{error}</span>}
            <div className="form-group">
                <label className='label' htmlFor="nombre">Nombre de curso:</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese el nombre**" id="nombre"
                    value={nombre_curso} onChange={e => setNombreCurso(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="descripcion">Descripción de curso:</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese una descripción corta**" id="descripcion"
                    value={descripcion} onChange={e => setDescripcionCurso(e.target.value)} />
            </div>
            <Button type="submit" variant="success">Guardar</Button>
        </form>
    );

}


/* FORMULARIO DE NIVEL */
export function FormularioNivel() {
    /* *** Form **** */
    const [nombre, setNombre] = useState("");
    const [descripcion, setDescripcion] = useState("");
    const [numero_categorias, setNumeroCategorias] = useState(0);
    const [grado_dificultad, setGradoDificultad] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const enviarN = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!isValidForm()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        //Flujo normal
        try {
            // Obtenemos los datos
            const datos__post = {
                nombre,
                descripcion,
                numero_categorias,
                grado_dificultad
            };
            console.log(datos__post);
            // Realizar la petición POST al servidor
            await guardar(datos__post);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar nivel');
            }
        }
    };

    // Funcion para guardar
    const guardar = async (datos__post) => {
        try {
            const response = await CrearNivelNew(datos__post);
            if (response.data.success) {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                Swal.fire("Nivel registrado correctamente", "", "success");
                navigate('/nivel/all');
            } else {
                if (response.data.error) {
                    Swal.fire(response.data.error, '', 'error')
                } else {
                    mostrarError('Error al registrar nivel');
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar nivel');
            }
        }
    }

    // Campos vacios
    const isValidForm = () => {
        if (
            nombre.trim() === "" ||
            descripcion.trim() === "" ||
            !numero_categorias ||
            grado_dificultad.trim() === ""
        ) {
            return false;
        }
        return true;
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <form onSubmit={enviarN}>
            {error && <span>{error}</span>}
            <div className="form-group">
                <label className='label' htmlFor="nombre">Nombre de nivel:</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese el nombre**" id="nombre"
                    value={nombre} onChange={e => setNombre(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="descripcion">Descripción de nivel:</label>
                <input onClick={info__nivel} className='form-control w-100' type="text" placeholder="Ingrese una descripción corta**" id="descripcion"
                    value={descripcion} onChange={e => setDescripcion(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="categoria">Número de categorías:</label>
                <input className='form-control w-100' type="number" id="categoria" name='categoria'
                    min='1' max='10' placeholder="Ingrese el número de categorías**"
                    value={numero_categorias} onChange={e => setNumeroCategorias(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="grado">Grado de dificultad:</label>
                <select className="form-control w-100" id="grado"
                    name="grado" value={grado_dificultad} onChange={e => setGradoDificultad(e.target.value)}>
                    <option value="none">None</option>
                    <option value="Leve"> Nivel leve</option>
                    <option value="Medio">Nivel medio</option>
                    <option value="Moderado">Nivel moderado</option>
                </select>
            </div>
            <Button type="submit" variant="success">Guardar</Button>
        </form>
    );
}


/* FORMULARIO DE DOMINIO */
export function FormularioDominio() {
    /* *** Form **** */
    const [nombre, setNombre] = useState("");
    const [descripcion, setDescripcion] = useState("");
    const [portada_dominio, setPortada] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Operacion de guardado
    const enviarD = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!isValidForm()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        //Flujo normal
        try {
            const formData = new FormData(); // Crear un objeto FormData
            formData.append('nombre', nombre);
            formData.append('descripcion', descripcion);
            formData.append('portada_dominio', portada_dominio);
            // Realizar la petición POST al servidor
            await guardar(formData);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar dominio');
            }
        }
    };

    // Funcion para guardar
    const guardar = async (formData) => {
        try {
            const response = await CrearDominioNew(formData);
            if (response.data.success) {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                navigate('/dominio/all');
            } else {
                if (response.data.error) {
                    Swal.fire(response.data.error, '', 'error')
                } else {
                    mostrarError('Error al registrar dominio');
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar dominio');
            }
        }
    }

    // Campos vacios
    const isValidForm = () => {
        if (
            nombre.trim() === "" ||
            descripcion.trim() === "" ||
            !portada_dominio
        ) {
            return false;
        }
        return true;
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <form onSubmit={enviarD} encType='multipart/form-data'>
            {error && <span>{error}</span>}
            <div className="form-group">
                <label className='label' htmlFor="nombre">Nombre de dominio:</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese el nombre**" id="nombre"
                    value={nombre} onChange={e => setNombre(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="descripcion">Descripción:</label>
                <input onClick={info__dominio} className='form-control w-100' type="text" placeholder="Ingrese una descripción corta**" id="descripcion"
                    value={descripcion} onChange={e => setDescripcion(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="portada_dominio">Portada:</label>
                <input className='form-control w-100' type="file" id="portada_dominio"
                    onChange={e => { setPortada(e.target.files[0]); validarTamanoImagen(e.target) }} name='portada_dominio' accept="image/*" />
            </div>
            <Button type="submit" variant="success">Guardar</Button>
        </form>
    )
}


/* FORMULARIO PETICION */
export function FormularioPeticion() {
    /* *** Form **** */
    const [motivo, setMotivo] = useState("");
    const [tipo, setTipo] = useState("");
    const [peticion_cuerpo, setPeticionCuerpo] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Operacion de guardado
    const enviarPeticion = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!isValidForm()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        //Flujo normal
        try {
            const formData = new FormData(); // Crear un objeto FormData
            formData.append('motivo', motivo);
            formData.append('peticion_cuerpo', peticion_cuerpo);
            formData.append('tipo', tipo);
            // Realizar la petición POST al servidor
            await guardar(formData);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar petición');
            }
        }
    };

    // Funcion para guardar 
    const guardar = async (formData) => {
        try {
            const response = await CrearPeticion(formData);
            if (response.data.success) {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                Swal.fire("Peticion registrada correctamente", "", "success");
                navigate('/nivel/all');
            } else {
                if (response.data.error) {
                    Swal.fire(response.data.error, '', 'error')
                } else {
                    mostrarError('Error al registrar petición');
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar petición');
            }
        }
    }

    // Campos vacios
    const isValidForm = () => {
        if (
            motivo.trim() === "" ||
            tipo.trim() === "" ||
            peticion_cuerpo.trim() === ""
        ) {
            return false;
        }
        return true;
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    return (
        <form onSubmit={enviarPeticion} encType='multipart/form-data'>
            {error && <span>{error}</span>}
            <div className="form-group">
                <label className='label' htmlFor="motivo">Motivo de petición:</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese el motivo**" id="motivo"
                    name="motivo" value={motivo} onChange={e => setMotivo(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="tipo">Selecciona el tipo:</label>
                <select className="form-control w-100" id="tipo"
                    name="tipo" value={tipo} onChange={e => setTipo(e.target.value)}>
                    <option value="none">----</option>
                    <option value="Editar">Edición</option>
                    <option value="Eliminar">Eliminación</option>
                    <option value="Agregar">Agregación</option>
                </select>
            </div>
            {/*}
            <div className="form-group">
                <label className='label' htmlFor="peticion_cuerpo">Archivo de petición:</label>
                <input className='form-control w-100' type="file" id="peticion_cuerpo"
                    onChange={e => { setPeticionCuerpo(e.target.files[0]) }} name='peticion_cuerpo'
                    accept="application/pdf" />
            </div>
            */}
            <div className="form-group">
                <label className='label' htmlFor="peticion_cuerpo">Descripción de petición:</label>
                <textarea className='form-control w-100 h-100' type="text" id="peticion_cuerpo"
                    value={peticion_cuerpo} onChange={e => setPeticionCuerpo(e.target.value)}
                    name='peticion_cuerpo' />
            </div>
            <Button type="submit" variant="success">Guardar</Button>
        </form>
    )
}


/* FORMULARIO SALA */
export function FormularioSala() {
    /* *** Form **** */
    const [nombre_sala, setNombre] = useState("");
    const [nombre_sala_n, setNombreN] = useState("");
    const [anotaciones, setAnotaciones] = useState("");
    const [codigo_identificador, setCodigo] = useState(0);
    const [nombre_paciente, setNombrePaciente] = useState("");
    const [error, setError] = useState("");
    const [entradaValida, setEntradavaldia] = useState(true);
    const navigate = useNavigate();

    // Operacion de guardado
    const enviarFSala = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!isValidForm()) {
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
            // Obtenemos los datos
            const datos__post = {
                nombre_sala,
                nombre_sala_n,
                anotaciones,
                codigo_identificador,
                nombre_paciente
            };
            // Funcion de registro
            await confirmGuardado(datos__post);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar sala');
            }
        }
    };

    // Campos vacios
    const isValidForm = () => {
        if (
            nombre_sala.trim() === "" ||
            anotaciones.trim() === "" ||
            !codigo_identificador ||
            nombre_paciente.trim() === ""
        ) {
            return false;
        }
        return true;
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Registro de sala
    const confirmGuardado = async (datos__post) => {
        return Swal.fire({
            title: '¿Desea guardar los datos de sala?',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: 'Guardar',
            denyButtonText: 'No guardar',
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    // Realizar la petición POST al servidor
                    const response = await CrearSalaNueva(datos__post);
                    if (response.data.success) {
                        // Redireccionar a la página principal si el inicio de sesión es exitoso
                        Swal.fire("Sala registrada correctamente", "", "success");
                        navigate('/sala/all');
                    } else {
                        if (response.data.error) {
                            Swal.fire(response.data.error, '', 'error');
                        } else {
                            Swal.fire('Error al registrar', '', 'error');
                        }
                    }
                } catch (error) {
                    Swal.fire('Error al registrar', '', 'error');
                }
            } else if (result.isDenied) {
                Swal.fire('Los datos no se guardaron', '', 'info');
                navigate('/nivel/all')
            }
        });
    };

    // Funcion para validar la entreada
    const cambioEntrada = (e) => {
        const value = e.target.value;
        setNombrePaciente(value);

        if (!validarEntrada(value)) {
            setEntradavaldia(false);
        } else {
            setEntradavaldia(true);
        }
    };

    // Validar entrada
    const validarEntrada = (value) => {
        const generar = /^[a-zA-Z]+ [a-zA-Z]+$/;
        return generar.test(value);
    };

    // Normalizar texto
    function normalizeText(text) {
        return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    const cambioNombre = (event) => {
        const valor = event.target.value;
        setNombre(valor);
        setNombreN(normalizeText(valor));
    };

    return (
        <form onSubmit={enviarFSala}>
            {error && <span>{error}</span>}
            <div className="form-group">
                <label className='label' htmlFor="nombre">Nombre de sala:</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese el nombre de sala**" id="nombre"
                    name="nombre" value={nombre_sala} onChange={cambioNombre} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="anotacion">Descripción de actividad:</label>
                <textarea className='form-control w-100 h-100' type="text" id="anotacion"
                    value={anotaciones} onChange={e => setAnotaciones(e.target.value)}
                    name='anotacion' />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="identificador">Identificador del contenido:</label>
                <input className='form-control w-100' type="number" placeholder="Ingrese el código de contenido**" id="identificador"
                    name="identificador" value={codigo_identificador} onChange={e => setCodigo(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="paciente">Nombre de paciente:</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese el nombre ejm: Luis Chavez**" id="paciente"
                    name="paciente" value={nombre_paciente} onChange={cambioEntrada} />
            </div>

            <Button type="submit" variant="success">Guardar</Button>
        </form>
    )

}


/* FORMULARIO SALA */
export function FormularioPeticionRevision() {
    /* *** Form **** */
    const [vereficto, setVeredicto] = useState("");
    const [estadoR, setEstadoR] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();
    // Capturamos el id de la url
    let { slug } = useParams();

    // Operacion de guardado
    const enviarFRevision = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!isValidForm()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            // Obtenemos los datos
            const datos__post = {
                vereficto,
                estadoR,
                slug
            };
            // Funcion de registro
            await confirmGuardado(datos__post);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/login');
            } else {
                mostrarError('Error al registrar revisión de sala');
            }
        }
    };

    // Campos vacios
    const isValidForm = () => {
        if (
            vereficto.trim() === "",
            estadoR.trim() === ""
        ) {
            return false;
        }
        return true;
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Registro de sala
    const confirmGuardado = async (datos__post) => {
        return Swal.fire({
            title: '¿Desea guardar la revisión de sala?',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: 'Guardar',
            denyButtonText: 'No guardar',
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    // Realizar la petición POST al servidor
                    const response = await AtenderPeticion(datos__post);
                    if (response.data.success) {
                        // Redireccionar a la página principal si el inicio de sesión es exitoso
                        Swal.fire("Revisión registrada correctamente", "", "success");
                        navigate('/peticion/all');
                    } else {
                        if (response.data.error) {
                            Swal.fire(response.data.error, '', 'error');
                        } else if (response.data.errorSalida) {
                            navigate('/login');
                        } else {
                            Swal.fire('Error al registrar', '', 'error');
                        }
                    }
                } catch (error) {
                    Swal.fire('Error al registrar', '', 'error');
                }
            } else if (result.isDenied) {
                Swal.fire('La revisión no se ha enviado', '', 'info');
                navigate('/peticion/all')
            }
        });
    };

    return (
        <form onSubmit={enviarFRevision}>
            {error && <span>{error}</span>}
            <div className="form-group">
                <label className='label' htmlFor="veredicto">Ingrese la decisión de la revisión :</label>
                <textarea className='form-control w-100' placeholder="Ingrese la decisión**" id="veredicto"
                    name="veredicto" value={vereficto} onChange={e => setVeredicto(e.target.value)} cols="30" rows="20">

                </textarea>
            </div>
            <div className="form-group">
                <label className='label' htmlFor="estado">Estado de revisión:</label>
                <select className="form-control w-100" id="estado"
                    name="estado" value={estadoR} onChange={e => setEstadoR(e.target.value)}>
                    <option value="none">None</option>
                    <option value="Aprobado">Aprobado</option>
                    <option value="Rechazado">Rechazado</option>
                </select>
            </div>
            <Button type="submit" variant="success">Enviar</Button>
        </form>
    )

}


// Formulario de confirmacion de cuenta
export function FormularioConfirmacion() {
    /* *** Form **** */
    const [tokenVerificacion, setToken] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Operacion de guardado
    const enviarFConfirmacion = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!valoresValidos()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            // Obtenemos los datos
            const datos__post = {
                tokenVerificacion
            };
            // Funcion de registro
            await confirmGuardado(datos__post);
        } catch (err) {
            mostrarError('Error al verificar cuenta');
        }
    };

    // Campos vacios
    const valoresValidos = () => {
        if (
            tokenVerificacion.trim() === ""
        ) {
            return false;
        }
        return true;
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 5000);
    };

    // Registro de sala
    const confirmGuardado = async (datos__post) => {
        return Swal.fire({
            title: '¿Desea verificar el registro de cuenta?',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: 'Verificar',
            denyButtonText: 'No verificar',
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    // Realizar la petición POST al servidor
                    const response = await VerificarCuenta(datos__post);
                    if (response.data.success) {
                        // Redireccionar a la página principal si el inicio de sesión es exitoso
                        Swal.fire("Verificación registrada correctamente", "", "success");
                        navigate('/login');
                    } else {
                        if (response.data.error) {
                            Swal.fire(response.data.error, '', 'error');
                            navigate('/login')
                        } else {
                            Swal.fire('Error al verificar', '', 'error');
                            navigate('/login')
                        }
                    }
                } catch (err) {
                    Swal.fire('Error al verificar', '', 'error');
                    navigate('/login')
                }
            } else if (result.isDenied) {
                Swal.fire('La verificación no se ha enviado', '', 'info');
                navigate('/login')
            }
        });
    };

    return (
        <form onSubmit={enviarFConfirmacion}>
            {error && <span>{error}</span>}
            <div className="form-group">
                <label className='label' htmlFor="codigo">Ingrese el código proporcionado :</label>
                <input className='form-control w-100' type="text" placeholder="Ingrese el código**" id="codigo"
                    name="codigo" value={tokenVerificacion} onChange={e => setToken(e.target.value)} />
            </div>
            <Button type="submit" variant="success">Verificar</Button>
        </form>
    )

}
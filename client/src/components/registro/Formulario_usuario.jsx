/* ******** FORMULARIO DE REGISTRO ******* */
// Estilos
import "bootstrap/dist/css/bootstrap.min.css"
// Componentes
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'
import Swal from "sweetalert2";
// Metodos
import {
    UsuarioCrearNuevo, VerificarUsuario, UsuarioIndividual, UsuarioEditar,
    CrearComunNew, ComunIndividual, ComunEditar, CrearPaciente, PacienteIndividual,
    PacienteEditar
} from "../../api/usuario.api";

/* FORMULARIO TECNICO */
export function FormularioUsuario() {
    /* *** Form **** */
    const token = localStorage.getItem('token');
    const [datos, setDatos] = useState([]);
    const [nombre_usuario, setNombre] = useState("");
    const [apellido_usuario, setApellido] = useState("");
    const [email_usuario, setEmail] = useState("");
    const [username_usuario, setUsername] = useState("");
    const [password_usuario, setPassword] = useState("");
    const [celular, setCelular] = useState("");
    const [fecha_nacimiento, setFecha] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // OPERACIONES
    const enviarFT = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (isEmptyField(nombre_usuario, apellido_usuario, email_usuario, username_usuario,
            password_usuario, celular, fecha_nacimiento)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            if (token) {
                const datos__edit = {
                    nombre_usuario,
                    apellido_usuario,
                    email_usuario,
                    celular,
                    fecha_nacimiento
                };
                // Llamamos a la función de editar usuario
                await confirmEdicion(datos__edit);
            } else {
                const datos__post = {
                    nombre_usuario,
                    apellido_usuario,
                    email_usuario,
                    username_usuario,
                    password_usuario,
                    celular,
                    fecha_nacimiento
                };
                // Realizar la petición POST al servidor
                guardar(datos__post);
            }
        } catch (error) {
            mostrarError('Error al registrar usuario');
        }
    };

    // Funcion para guardar datos
    const guardar = async (datos__post) => {
        const response = await UsuarioCrearNuevo(datos__post);
        // Confirmar operación
        if (response.data.success) {
            navigate('/login');
        } else {
            if (response.data.error) {
                Swal.fire(response.data.error, '', 'error');
            } else if (response.data.clave) {
                Swal.fire(response.data.clave, '', 'error');
                mostrarError('La clave debe tener mínimo 8 caracteres que incluye una letra mayúscula, un número y un símbolo');
            } else {
                mostrarError('Datos no válidos');
            }
        }
    }

    // Obtener datos de tecnico
    const obtenerDatosUsuario = async () => {
        try {
            const cont = await VerificarUsuario();
            if (cont.data.success) {
                setDatos(cont.data);
                const datos__user = await UsuarioIndividual(cont.data.identificador);
                setNombre(datos__user.data.nombre_usuario);
                setApellido(datos__user.data.apellido_usuario);
                setEmail(datos__user.data.email_usuario);
                setUsername(datos__user.data.username_usuario);
                setPassword("---");
                setCelular(datos__user.data.celular);
                setFecha(datos__user.data.fecha_nacimiento);
                console.log(datos__user.data);
            } else {
                if (cont.data.error) {
                    Swal.fire(cont.data.error, '', 'error');
                } else {
                    navigate('/login');
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al mostrar datos de usuario');
            }
        }
    }
    // Use effect
    useEffect(() => {
        if (token) {
            obtenerDatosUsuario();
        } else {
            navigate('/login');
        }
    }, []);

    // Edicion
    const confirmEdicion = async (datos__edit) => {
        return Swal.fire({
            title: '¿Desea guardar los cambios en su perfil?',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: 'Actualizar',
            denyButtonText: 'No guardar',
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    await UsuarioEditar(datos.identificador, datos__edit);
                    Swal.fire("Datos actualizados", "", "success");
                    navigate('/perfil');
                } catch (error) {
                    Swal.fire('Error al actualizar', '', 'error');
                }
            } else if (result.isDenied) {
                Swal.fire('Los cambios no se guardaron', '', 'info');
                navigate('/perfil');
            }
        });
    };

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 9000); // 8 segundos
    };

    return (
        <form onSubmit={enviarFT}>
            <>
                {error && <span>{error}</span>}
            </>
            <div className='form-row row mt-1'>
                <div className="form-group col-md-6">
                    <label className='label' htmlFor="nombre">Nombre:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el nombre**" name='nombre' id="nombre"
                        value={nombre_usuario} onChange={e => setNombre(e.target.value)} autoFocus />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="apellido">Apellido:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el apellido**" name='apellido' id="apellido"
                        value={apellido_usuario} onChange={e => setApellido(e.target.value)}
                    />
                </div>
            </div>
            <div className='form-row row'>
                <div className="form-group col-md-6">
                    <label className='label' htmlFor="email"> Correo Electrónico::</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el correo electrónico**" name='email' id="email"
                        value={email_usuario} onChange={e => setEmail(e.target.value)} />
                </div>
                <div className="form-group col-md-6">
                    <label className='label' htmlFor="username">Usuario:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el username**" name='username' id="username"
                        value={username_usuario} onChange={e => setUsername(e.target.value)} />
                </div>
            </div>
            <>
                {
                    !datos?.tipo &&
                    <div className='form-group'>
                        <label className='label' htmlFor="password">Clave:</label>
                        <input className='form-control w-100' type="password"
                            placeholder="Mínimo 8 caracteres con una letra mayúscula, un número y un símbolo**"
                            name='password' id="password"
                            value={password_usuario} onChange={e => setPassword(e.target.value)} />
                    </div>
                }
            </>
            <div className='form-row row'>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="celular">Número de teléfono:</label>
                    <input className='form-control w-100' maxLength={10} type="text" placeholder="Ingrese el número de celular**" name='celular' id="celular"
                        value={celular}
                        onChange={e => {
                            // Comprobar si la entrada es un número o si es un backspace/delete
                            if (e.target.value === "" || /^[0-9\b]+$/.test(e.target.value)) {
                                setCelular(e.target.value);
                            }
                        }} />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="fecha">Fecha de nacimiento:</label>
                    <input className='form-control w-100' maxLength={10} type="date" name='fecha' id="fecha"
                        value={fecha_nacimiento} onChange={e => setFecha(e.target.value)} />
                </div>
            </div>
            <button type='submit' className='btn btn-success'>Guardar</button>
        </form>
    )
}


/* FORMULARIO COMUN */
export function FormularioComun() {
    /* *** Form **** */
    const token = localStorage.getItem('token');
    const [datos, setDatos] = useState([]);
    const [nombre_usuario, setNombre] = useState("");
    const [apellido_usuario, setApellido] = useState("");
    const [email_usuario, setEmail] = useState("");
    const [username_usuario, setUsername] = useState("");
    const [password_usuario, setPassword] = useState("");
    const [celular, setCelular] = useState("");
    const [fecha_nacimiento, setFecha] = useState("");
    const [genero, setGenero] = useState("");
    const [area_estudio, setAreaEstudio] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Operacion de guardar datos
    const enviarFComun = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (isEmptyField(nombre_usuario, apellido_usuario, email_usuario, username_usuario,
            password_usuario, celular, fecha_nacimiento, genero, area_estudio)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }

        // Flujo normal
        try {
            if (token) {
                const datos__edit = {
                    nombre_usuario,
                    apellido_usuario,
                    email_usuario,
                    username_usuario,
                    celular,
                    fecha_nacimiento,
                    genero,
                    area_estudio
                }
                // Llamamos a la función de editar usuario
                await confirmEdicion(datos__edit);
            } else {
                const datos__post = {
                    nombre_usuario,
                    apellido_usuario,
                    email_usuario,
                    username_usuario,
                    password_usuario,
                    celular,
                    fecha_nacimiento,
                    genero,
                    area_estudio
                };
                // Realizar la petición POST al servidor
                guardar(datos__post);
            }
        } catch (error) {
            mostrarError('Error al registrar usuario');
        }
    };

    // Guardar datos
    const guardar = async (datos__post) => {
        const response = await CrearComunNew(datos__post);
        // Confirmar operación
        if (response.data.success) {
            navigate('/login');
        } else {
            if (response.data.error) {
                Swal.fire(response.data.error, '', 'error');
            } else if (response.data.clave) {
                Swal.fire(response.data.clave, '', 'error');
                mostrarError('La clave debe tener mínimo 8 caracteres que incluye una letra mayúscula, un número y un símbolo');
            } else {
                mostrarError('Datos no válidos');
            }

        }
    }

    // Obtener datos de comun
    const obtenerDatosComun = async () => {
        try {
            const contUC = await VerificarUsuario();
            if (contUC.data.success) {
                setDatos(contUC.data);
                const datos__user = await ComunIndividual(contUC.data.identificador);
                setNombre(datos__user.data.nombre_usuario);
                setApellido(datos__user.data.apellido_usuario);
                setEmail(datos__user.data.email_usuario);
                setUsername(datos__user.data.username_usuario);
                setPassword("---");
                setCelular(datos__user.data.celular);
                setFecha(datos__user.data.fecha_nacimiento);
                setGenero(datos__user.data.genero);
                setAreaEstudio(datos__user.data.area_estudio);
            } else {
                if (contUC.data.error) {
                    Swal.fire(contUC.data.error, '', 'error');
                } else {
                    navigate('/login');
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al mostrar datos de usuario');
            }
        }
    }
    // Use Effect
    useEffect(() => {
        if (token) {
            obtenerDatosComun();
        }
    }, []);

    // Edicion
    const confirmEdicion = async (datos__edit) => {
        return Swal.fire({
            title: '¿Desea guardar los cambios en su perfil?',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: 'Actualizar',
            denyButtonText: 'No guardar',
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    await ComunEditar(datos.identificador, datos__edit);
                    Swal.fire("Datos actualizados", "", "success");
                    navigate('/perfil');
                } catch (error) {
                    Swal.fire('Error al actualizar', '', 'error');
                }
            } else if (result.isDenied) {
                Swal.fire('Los cambios no se guardaron', '', 'info');
                navigate('/perfil');
            }
        });
    };

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 9000); // 8 segundos
    };

    return (
        <form onSubmit={enviarFComun}>
            <>
                {error && <span>{error}</span>}
            </>
            <div className='form-row row mt-1'>
                <div className="form-group col-md-6">
                    <label className='label' htmlFor="nombre">Nombre:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el nombre**" name='nombre' id="nombre"
                        value={nombre_usuario} onChange={e => setNombre(e.target.value)} autoFocus />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="apellido">Apellido:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el apellido**" name='apellido' id="apellido"
                        value={apellido_usuario} onChange={e => setApellido(e.target.value)}
                    />
                </div>
            </div>
            <div className='form-row row'>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="email"> Correo Electrónico::</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el correo electrónico**" name='email' id="email"
                        value={email_usuario} onChange={e => setEmail(e.target.value)} />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="username">Usuario:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el username**" name='username' id="username"
                        value={username_usuario} onChange={e => setUsername(e.target.value)} />
                </div>
            </div>
            <>
                {
                    !datos?.tipo &&
                    <div className='form-group'>
                        <label className='label' htmlFor="password">Clave:</label>
                        <input className='form-control w-100' type="password"
                            placeholder="Mínimo 8 caracteres con una letra mayúscula, un número y un símbolo**"
                            name='password' id="password"
                            value={password_usuario} onChange={e => setPassword(e.target.value)} />
                    </div>
                }

            </>
            <div className='form-row row'>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="celular">Número de teléfono:</label>
                    <input className='form-control w-100' maxLength={10} type="text" placeholder="Ingrese el número de celular**" name='celular' id="celular"
                        value={celular}
                        onChange={e => {
                            if (e.target.value === "" || /^[0-9\b]+$/.test(e.target.value)) {
                                setCelular(e.target.value);
                            }
                        }} />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="fecha">Fecha de nacimiento:</label>
                    <input className='form-control w-100' maxLength={10} type="date" name='fecha' id="fecha"
                        value={fecha_nacimiento} onChange={e => setFecha(e.target.value)} />
                </div>
            </div>
            <div className='form-row row'>
                <div className="form-group col-md-6">
                    <label className='label' htmlFor="genero">Género:</label>
                    <select className="form-control w-100" id="genero"
                        name="genero" value={genero} onChange={e => setGenero(e.target.value)}>
                        <option value="none">----</option>
                        <option value="Masculino">Soy chico</option>
                        <option value="Femenino">Soy chica</option>
                        <option value="Otro">Prefiero no decirlo</option>
                    </select>
                </div>
                <div className="form-group col-md-6">
                    <label className='label' htmlFor="area">Área de estudio:</label>
                    <select className="form-control w-100" id="area"
                        name="area" value={area_estudio} onChange={e => setAreaEstudio(e.target.value)}>
                        <option value="none">----</option>
                        <option value="Tecnico">Técnico</option>
                        <option value="Psicopedagogo">Psicopedagogo</option>
                    </select>
                </div>
            </div>
            <button type='submit' className='btn btn-success'>Guardar</button>
        </form>
    )

}


/* FORMULARIO PACIENTE */
export function FormularioPaciente() {
    /* *** Form **** */
    const token = localStorage.getItem('token');
    const [datos, setDatos] = useState([]);
    const [nombre_usuario, setNombre] = useState("");
    const [apellido_usuario, setApellido] = useState("");
    const [email_usuario, setEmail] = useState("");
    const [username_usuario, setUsername] = useState("");
    const [password_usuario, setPassword] = useState("");
    const [celular, setCelular] = useState("");
    const [fecha_nacimiento, setFecha] = useState("");
    const [contacto_emergencia, setContactoEmergencia] = useState("");
    const [direccion, setDireccion] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Operacion de guardar datos
    const enviarFP = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (isEmptyField(nombre_usuario, apellido_usuario, email_usuario, username_usuario,
            password_usuario, celular, fecha_nacimiento, contacto_emergencia, direccion)) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        // Flujo normal
        try {
            if (token) {
                const datos__edit = {
                    nombre_usuario,
                    apellido_usuario,
                    email_usuario,
                    username_usuario,
                    celular,
                    fecha_nacimiento,
                    contacto_emergencia,
                    direccion
                }
                // Llamamos a la función de editar usuario
                await confirmEdicion(datos__edit);
            } else {

                const datos__post = {
                    nombre_usuario,
                    apellido_usuario,
                    email_usuario,
                    username_usuario,
                    password_usuario,
                    celular,
                    fecha_nacimiento,
                    contacto_emergencia,
                    direccion
                };
                // Realizar la petición POST al servidor
                guardar(datos__post);
            }
        } catch (error) {
            mostrarError('Error al registrar usuario');
        }
    };

    // Guardar datos
    const guardar = async (datos__post) => {
        const response = await CrearPaciente(datos__post);
        // Confirmar operación
        if (response.data.success) {
            navigate('/login');
        } else {
            if (response.data.error) {
                Swal.fire(response.data.error, '', 'error');
            } else if (response.data.clave) {
                Swal.fire(response.data.clave, '', 'error');
                mostrarError('La clave debe tener mínimo 8 caracteres que incluye una letra mayúscula, un número y un símbolo');
            } else {
                mostrarError('Datos no válidos');
            }
        }
    }

    // Obtener datos de paciente
    const obtenerDatosP = async () => {
        try {
            const contP = await VerificarUsuario();
            if (contP.data.success) {
                setDatos(contP.data);
                const datos__user = await PacienteIndividual(contP.data.identificador);
                setNombre(datos__user.data.nombre_usuario);
                setApellido(datos__user.data.apellido_usuario);
                setEmail(datos__user.data.email_usuario);
                setUsername(datos__user.data.username_usuario);
                setCelular(datos__user.data.celular);
                setPassword("---");
                setContactoEmergencia(datos__user.data.contacto_emergencia);
                setFecha(datos__user.data.fecha_nacimiento);
                setDireccion(datos__user.data.direccion);
            } else {
                if (contP.data.error) {
                    Swal.fire(contP.data.error, '', 'error');
                } else {
                    navigate('/login');
                }
            }
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al mostrar datos de usuario');
            }
        }
    }
    // Use  effect
    useEffect(() => {
        if (token) {
            obtenerDatosP();
        }
    }, []);

    // Edicion
    const confirmEdicion = async (datos__edit) => {
        return Swal.fire({
            title: '¿Desea guardar los cambios en su perfil?',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: 'Actualizar',
            denyButtonText: 'No guardar',
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    await PacienteEditar(datos.identificador, datos__edit);
                    Swal.fire("Datos actualizados", "", "success");
                    navigate('/perfil');
                } catch (error) {
                    Swal.fire('Error al actualizar', '', 'error');
                }
            } else if (result.isDenied) {
                Swal.fire('Los cambios no se guardaron', '', 'info');
                navigate('/perfil');
            }
        });
    };

    // Control de entrada de datos
    const isEmptyField = (...fields) => {
        return fields.some(field => field.trim() === "");
    }

    // Mostrar error
    const mostrarError = (message) => {
        setError(message);
        setTimeout(() => {
            setError("");
        }, 9000);
    };

    return (
        <form onSubmit={enviarFP}>
            <>
                {error && <span>{error}</span>}
            </>
            <div className='form-row row mt-1'>
                <div className="form-group col-md-6">
                    <label className='label' htmlFor="nombre">Nombre:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el nombre**" name='nombre' id="nombre"
                        value={nombre_usuario} onChange={e => setNombre(e.target.value)} autoFocus />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="apellido">Apellido:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el apellido**" name='apellido' id="apellido"
                        value={apellido_usuario} onChange={e => setApellido(e.target.value)}
                    />
                </div>
            </div>
            <div className='form-row row'>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="email"> Correo Electrónico:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el correo electrónico**" name='email' id="email"
                        value={email_usuario} onChange={e => setEmail(e.target.value)} />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="username">Usuario:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese el username**" name='username' id="username"
                        value={username_usuario} onChange={e => setUsername(e.target.value)} />
                </div>
            </div>
            <>
                {
                    !datos?.tipo &&
                    <div className='form-group'>
                        <label className='label' htmlFor="password">Clave:</label>
                        <input className='form-control w-100' type="password"
                            placeholder="Mínimo 8 caracteres con una letra mayúscula, un número y un símbolo**"
                            name='password' id="password"
                            value={password_usuario} onChange={e => setPassword(e.target.value)} />
                    </div>
                }
            </>
            <div className='form-row row'>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="celular">Número de teléfono:</label>
                    <input className='form-control w-100' maxLength={10} type="text" placeholder="Ingrese celular**" name='celular' id="celular"
                        value={celular}
                        onChange={e => {
                            if (e.target.value === "" || /^[0-9\b]+$/.test(e.target.value)) {
                                setCelular(e.target.value);
                            }
                        }} />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="fecha">Fecha de nacimiento:</label>
                    <input className='form-control w-100' maxLength={10} type="date" name='fecha' id="fecha"
                        value={fecha_nacimiento} onChange={e => setFecha(e.target.value)} />
                </div>
            </div>
            <div className='form-row row'>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="contacto">Contacto de emergencia:</label>
                    <input className='form-control w-100' maxLength={10} type="text" placeholder="Contacto de emergencia**" name='contacto' id="contacto"
                        value={contacto_emergencia}
                        onChange={e => {
                            // Comprobar si la entrada es un número o si es un backspace/delete
                            if (e.target.value === "" || /^[0-9\b]+$/.test(e.target.value)) {
                                setContactoEmergencia(e.target.value);
                            }
                        }} />
                </div>
                <div className='form-group col-md-6'>
                    <label className='label' htmlFor="direccion">Dirección:</label>
                    <input className='form-control w-100' type="text" placeholder="Ingrese su dirección**" name='direccion' id="direccion"
                        value={direccion} onChange={e => setDireccion(e.target.value)}
                    />
                </div>
            </div>
            <button type='submit' className='btn btn-success'>Guardar</button>
        </form>
    )
}

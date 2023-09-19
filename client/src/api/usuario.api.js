import axios from 'axios';

const baseurl = axios.create({
    baseURL: 'http://localhost:8000/wapiptdah/',
})

/* ****  TECNICO **** */
export const UsuarioListado = () => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get('aplicacion/usuario/',
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

export const UsuarioCrear = (usuario) => baseurl.post('aplicacion/usuario/', usuario)

export const UsuarioCrearNuevo = async (datos__post) => {
    return await baseurl.post('registro_usuario/', datos__post);
};

// Editar usuario
export const UsuarioEditar = (id, usuario) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.put(`aplicacion/usuario/${id}/`, usuario,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

// Usuario individual
export const UsuarioIndividual = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`aplicacion/usuario/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};


/* ****  PACIENTE **** */

export const PacienteListado = () => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get('aplicacion/paciente/',
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

export const PacienteCrear = (paciente) => baseurl.post('aplicacion/paciente/', paciente)

// Crear paciente
export const CrearPaciente = async (datos__post) => {
    return await baseurl.post('registro_paciente/', datos__post);
};

// Editar paciente
export const PacienteEditar = (id, usuario) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.put(`aplicacion/paciente/${id}/`, usuario,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

// Paciente individual
export const PacienteIndividual = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`aplicacion/paciente/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

// Busqueda de salas
export const BusquedaPacientesCurso = (nombre, slug, page = 1) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`busqueda/paciente/curso/${encodeURIComponent(nombre)}/${slug}/?page=${page}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a las salas: " + error.message);
    }
};

/* ****  COMUN **** */
export const ComunListado = () => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get('aplicacion/comun/',
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

export const ComunCrear = (paciente) => baseurl.post('aplicacion/comun/', paciente)

// Crear usuario comun
export const CrearComunNew = async (datos__post) => {
    return await baseurl.post('registro_comun/', datos__post);
};

// Editar usuario comun
export const ComunEditar = (id, usuario) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.put(`aplicacion/comun/${id}/`, usuario,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

// Datos individuales de usuario comun
export const ComunIndividual = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`aplicacion/comun/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

/* *** METODOS COMUNES *** */
export const VerificarUsuario = async () => {
    const tokenLocal = localStorage.getItem('token');
    if (!tokenLocal) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return await baseurl.get('verificar/usuario/', {
            headers: {
                'Authorization': `Bearer ${tokenLocal}`
            }
        });
    } catch (error) {
        throw new Error("No se puede verificar al usuario: " + error.message);
    }
};

// Datos de usuario
export const DatosUser = async () => {
    const tokenLocal = localStorage.getItem('token');
    if (!tokenLocal) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return await baseurl.get('datos/usuario/', {
            headers: {
                'Authorization': `Bearer ${tokenLocal}`
                //'Authorization': `Token ${tokenLocal}`
            }
        });
    } catch (error) {
        throw new Error("No se puede acceder al usuario: " + error.message);
    }
};

// Eliminar usuario comun
export const UsuarioEliminar = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.delete(`aplicacion/user/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los usuarios: " + error.message);
    }
};

/* INSCRIPCIONES A CURSO*/
export const InscripcionCurso = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`registro/curso/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede inscribir en un curso: " + error.message);
    }
};



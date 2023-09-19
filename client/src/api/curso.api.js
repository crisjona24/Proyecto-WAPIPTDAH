// Objective: API for the course module
import axios from 'axios';

const baseurl = axios.create({
    baseURL: 'http://localhost:8000/',
})

/* Listado de cursos */
export const CursoListado = (page = 1) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/aplicacion/curso/?page=${page}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a cursos: " + error.message);
    }
};

// LISTA DE CURSOS DE UN USUARIO
export const CursosUsuarioComun = (page = 1) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/lista/cursos/?page=${page}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los cursos del usuario: " + error.message);
    }
};

/* Crear un nuevo curso */
export const CursoCrear = (curso) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.post('wapiptdah/aplicacion/curso/', curso,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede crear el curso: " + error.message);
    }
};

/* Crear curso manualmente */
export const CrearCurso = async (datos__post) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return await baseurl.post('wapiptdah/registro_curso/', datos__post, {
            headers: {
                'Authorization': `Bearer ${token}`
                //'Authorization': `Token ${token}`
            }
        });
    } catch (error) {
        throw new Error("No se puede crear el curso: " + error.message);
    }
};

/* Datos individuales */
export const CursoIndividual = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/aplicacion/curso/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder al curso: " + error.message);
    }
};

/* Actualizar curso */
export const CursoEditar = (id, curso) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.put(`wapiptdah/aplicacion/curso/${id}/`, curso,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede editar el curso: " + error.message);
    }
};

/* Eliminar curso */
export const CursoEliminar = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.delete(`wapiptdah/aplicacion/curso/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede eliminar el curso: " + error.message);
    }
};

/* *** METODOS COMUNES *** */
export const VerificarCurso = async (slug) => {
    const tokenLocal = localStorage.getItem('token');
    if (!tokenLocal) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return await baseurl.get(`wapiptdah/verificar/curso/${slug}/`, {
            headers: {
                'Authorization': `Bearer ${tokenLocal}`
                //'Authorization': `Token ${tokenLocal}`
            }
        });
    } catch (error) {
        throw new Error("No se puede verificar el curso: " + error.message);
    }
}

export const VerificarInscripcion = () => {
    const tokenLocal = localStorage.getItem('token');
    if (!tokenLocal) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get('wapiptdah/verificar/inscripcion/', {
            headers: {
                'Authorization': `Bearer ${tokenLocal}`
                //'Authorization': `Token ${tokenLocal}`
            }
        });
    } catch (error) {
        throw new Error("No se puede verificar la inscripción: " + error.message);
    }
}

export const PacientesInscritos = (id, page = 1) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/lista/pacientes/${id}/?page=${page}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los pacientes: " + error.message);
    }
};

// Obtener slug de curso
export const ObtenerSlugCurso = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/obtener/curso/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a los pacientes: " + error.message);
    }
};

// Busqueda de curso
export const BusquedaCurso = (nombre, page = 1) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/busqueda/curso/${encodeURIComponent(nombre)}/?page=${page}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a las salas: " + error.message);
    }
};
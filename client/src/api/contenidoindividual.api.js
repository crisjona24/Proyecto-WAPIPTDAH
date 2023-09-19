import axios from 'axios';

const baseurl = axios.create({
    baseURL: 'http://localhost:8000/',
})

// Listas
export const ContenidoIndividualListado = (page = 1) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/aplicacion/contenido_individual/?page=${page}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede listar los contenidos: " + error.message);
    }
};

export const IndividualListEspecifico = (slug, page = 1) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/contenidos/individuales/${slug}/?page=${page}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a contenidos: " + error.message);
    }
};

export const IndividualListNombre = (slug, nombre, page = 1) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/contenidos/individuales/nombre/${slug}/${nombre}/?page=${page}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a contenidos: " + error.message);
    }
};

// Crear contenido individual
export const ContenidoIndividualCrear = (contenido) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.post('wapiptdah/aplicacion/contenido_individual/', contenido,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede crear el contenido: " + error.message);
    }
};

export const CrearContenidoIndividual = async (datos__post) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return await baseurl.post('wapiptdah/registro_contenido_individual/', datos__post,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            });
    } catch (error) {
        throw new Error("No se puede crear el contenido: " + error.message);
    }
}

// Cargar contenido individual
export const CargarContenido = async (slug) => {
    // EL SLUG PROVIENE DE CONTENIDO INDIVIDUAL O CONTENIDO GENERAL
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return await baseurl.get(`wapiptdah/cargar_contenido_individual/${slug}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            });
    } catch (error) {
        throw new Error("No se puede cargar el contenido: " + error.message);
    }
}

export const ContenidoDatosIndividual = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/aplicacion/contenido_individual/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder al registro de contenido: " + error.message);
    }
}

// Editar contenido individual
export const ContenidoIndividualEditar = (id, contenido) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.put(`wapiptdah/aplicacion/contenido_individual/${id}/`, contenido,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede editar el contenido: " + error.message);
    }
}

/* *** METODOS COMUNES *** */
export const VerificarContenidoIndividual = async (slug) => {
    const tokenLocal = localStorage.getItem('token');
    if (!tokenLocal) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return await baseurl.get(`wapiptdah/verificar/contenido/individual/${slug}/`,
            {
                headers: {
                    'Authorization': `Bearer ${tokenLocal}`
                    //'Authorization': `Token ${tokenLocal}`
                }
            });
    } catch (error) {
        throw new Error("No se puede verificar el contenido: " + error.message);
    }
}

export const IndividualEliminar = (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.delete(`wapiptdah/aplicacion/contenido_individual/${id}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede eliminar el contenido: " + error.message);
    }
}

// Slug de dominio
export const ObtenerSlugDominio = (slug) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/obtener/dominio/${slug}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a contenidos: " + error.message);
    }
};

// Slug de contenido
export const ObtenerSlugContenido = (slug) => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error("NOT_AUTHENTICATED");
    }
    try {
        return baseurl.get(`wapiptdah/obtener/contenido/${slug}/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                    //'Authorization': `Token ${token}`
                }
            })
    } catch (error) {
        throw new Error("No se puede acceder a contenidos: " + error.message);
    }
};
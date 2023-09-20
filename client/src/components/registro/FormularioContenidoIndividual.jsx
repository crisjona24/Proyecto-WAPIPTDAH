// Estilos
import Button from 'react-bootstrap/Button';
import "bootstrap/dist/css/bootstrap.min.css"
// Componentes
import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Swal from "sweetalert2";
// Metodos
import { CrearContenidoIndividual } from '../../api/contenidoindividual.api';
import { ContenidoListadoSolo } from '../../api/contenido.api';
import { NivelListado } from '../../api/grado.api';
import { validarTamanoImagen } from '../../controles/alert_user';
import { info__contenido, info__contenido__respuesta } from '../../controles/controlador_registro';

export function FormularioContenidoIndividual({ slug }) {
    /* *** Form **** */
    const [niveles, setNiveles] = useState([]);
    const [nombre_nivel, setNombreNivel] = useState("");
    const [contenidos, setContenidos] = useState([]);
    const [conten, setConten] = useState("");
    const [descripcion_individual, setDescripcion] = useState("");
    const [tipo_contenido, setTipo] = useState("");
    const [contenido_individual, setContenido] = useState("");
    const [img1, setImg1] = useState("");
    const [img2, setImg2] = useState("");
    const [img3, setImg3] = useState("");
    const [portada_individual, setPortada] = useState("");
    const [respuesta, setRespuesta] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    const enviarFContenido = async (e) => {
        e.preventDefault();
        // Verificar campos vacíos
        if (!camposValidos()) {
            Swal.fire("Por favor ingrese todos los campos", "", "warning");
            return;
        }
        //Flujo normal
        try {
            const formData = new FormData(); // Crear un objeto FormData
            formData.append('descripcion_individual', descripcion_individual);
            formData.append('tipo_contenido', tipo_contenido);
            formData.append('respuesta', respuesta);
            formData.append('nombre_nivel', nombre_nivel);
            formData.append('contenido_individual', contenido_individual);
            formData.append('img1', img1);
            formData.append('img2', img2);
            formData.append('img3', img3);
            formData.append('portada_individual', portada_individual);
            formData.append('conten', conten);
            // Realizar la petición POST al servidor
            await guardarContenido(formData);
        } catch (error) {
            if (error.message === "NOT_AUTHENTICATED") {
                navigate('/');
            } else {
                mostrarError('Error al registrar contenido');
            }
        }
    };

    // Funcion para guardar
    const guardarContenido = async (formData) => {
        try {
            const response = await CrearContenidoIndividual(formData);
            if (response.data.success) {
                // Redireccionar a la página principal si el inicio de sesión es exitoso
                navigate(`/contenido/individual/all/${slug}/`);
            } else {
                if (response.data.error) {
                    mostrarError(response.data.error);
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
    // Cargar datos
    const cargarNivel = async () => {
        try {
            const nivel = await NivelListado();
            setNiveles(nivel.data);
        } catch (error) {
            mostrarError('Error al obtener datos de dominio');
        }
    };

    const cargarConten = async () => {
        try {
            const data = await ContenidoListadoSolo();
            setContenidos(data.data);
        } catch (error) {
            mostrarError('Error al obtener datos de dominio');
        }
    };

    // UseEffect
    useEffect(() => {
        if (!token) navigate('/login');
        cargarNivel();
        cargarConten();
    }, []);

    // Campos vacios
    const camposValidos = () => {
        if (
            descripcion_individual.trim() === "" ||
            tipo_contenido.trim() === "" ||
            respuesta.trim() === "" ||
            conten.trim() === "" ||
            nombre_nivel.trim() === "" ||
            !contenido_individual ||
            !portada_individual
        ) {
            return false;
        }
        if (tipo_contenido === "selecion_multiple_img" && (!img1 || !img2 || !img3)) {
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
        <form onSubmit={enviarFContenido} encType='multipart/form-data'>
            {error && <p>{error}</p>}
            <div className="form-group">
                <label className='label' htmlFor="descripcion">Indicación:</label>
                <input onClick={info__contenido} className='form-control w-100' type="text" placeholder="Ingresa la indicación de la actividad**" id="descripcion" name="descripcion"
                    value={descripcion_individual} onChange={e => setDescripcion(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="respuesta">Respuesta:</label>
                <input onClick={info__contenido__respuesta} className='form-control w-100' type="text" placeholder="Ingresa la respuesta**" id="respuesta" name="respuesta"
                    value={respuesta} onChange={e => setRespuesta(e.target.value)} />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="portada_individual">Portada:</label>
                <input className='form-control w-100' type="file" id="portada_individual"
                    onChange={(e) => { setPortada(e.target.files[0]); validarTamanoImagen(e.target) }} name='portada_individual' accept="image/*" />
            </div>
            <div className="form-group">
                <label className='label' htmlFor="tipo">Tipo de contenido:</label>
                <select className="form-control w-100" id="tipo" name="tipo"
                    value={tipo_contenido} onChange={e => setTipo(e.target.value)}>
                    <option value="none">None</option>
                    <option value="selecion_individual">Tipo 1 - Selección Individual</option>
                    <option value="verdadero_falso">Tipo 2 - Verdadero o Falso</option>
                    <option value="selecion_multiple">Tipo 3 - Selección Múltiple</option>
                    <option value="responder_preguntas">Tipo 4 - Responder Preguntas</option>
                    <option value="pintar_imagen">Tipo 5 - Colorear</option>
                    <option value="seleccionar_imagen">Tipo 6 - Selección de Imágenes</option>
                    <option value="cuento">Tipo 7 - Lectura Comprensiva</option>
                    <option value="juego_simple">Tipo 8 - Juegos Simples</option>
                    <option value="selecion_multiple_img">Tipo 9 - Selección Individual con imagen</option>
                </select>
            </div>
            <div className="form-group">
                <label className='label' htmlFor="contenido_individual">Contenido:</label>
                <input className='form-control w-100' type="file" id="contenido_individual"
                    onChange={(e) => { setContenido(e.target.files[0]); validarTamanoImagen(e.target) }}
                    name='contenido_individual' accept="image/*" />
            </div>
            {
                tipo_contenido === "selecion_multiple_img" &&
                <>
                    <div className="form-group">
                        <label className='label' htmlFor="img1">Contenido de opción 2:</label>
                        <input className='form-control w-100' type="file" id="img1"
                            onChange={(e) => { setImg1(e.target.files[0]); validarTamanoImagen(e.target) }}
                            name='img1' accept="image/*" />
                    </div>
                    <div className="form-group">
                        <label className='label' htmlFor="img2">Contenido de opción 3:</label>
                        <input className='form-control w-100' type="file" id="img2"
                            onChange={(e) => { setImg2(e.target.files[0]); validarTamanoImagen(e.target) }}
                            name='img2' accept="image/*" />
                    </div>
                    <div className="form-group">
                        <label className='label' htmlFor="img3">Contenido de opción 4:</label>
                        <input className='form-control w-100' type="file" id="img3"
                            onChange={(e) => { setImg3(e.target.files[0]); validarTamanoImagen(e.target) }}
                            name='img3' accept="image/*" />
                    </div>
                </>
            }
            <div className="form-group">
                <label className='label' htmlFor="conten">Pertenece a:</label>
                <select className="form-control w-100" id="conten"
                    name="conten" value={conten} onChange={e => setConten(e.target.value)}>
                    <option value="none">None</option>
                    <>
                        {contenidos.map((dominio) => (
                            <option key={dominio.id} value={dominio.nombre}>
                                {dominio.nombre}
                            </option>
                        ))}
                    </>
                </select>
            </div>
            <div className="form-group">
                <label className='label' htmlFor="grado">Grado:</label>
                <select className="form-control w-100" id="grado"
                    name="grado" value={nombre_nivel} onChange={e => setNombreNivel(e.target.value)}>
                    <option value="none">None</option>
                    <>
                        {niveles.map((nivel) => (
                            <option key={nivel.id} value={nivel.nombre_nivel}>
                                {nivel.nombre_nivel}
                            </option>
                        ))}
                    </>
                </select>
            </div>
            <Button type='submit' className='btn btn-success' >
                Guardar
            </Button>
        </form>
    )
}
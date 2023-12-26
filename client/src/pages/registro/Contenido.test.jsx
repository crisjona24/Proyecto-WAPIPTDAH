/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { ContenidoRegistro } from './ContenidoRegistro';
import { IndividualRegistro } from './ContenidoIndividualRegistro';
import { ContenidoEdición } from '../edicion/ContenidoEdicion';
import { IndividualEdición } from '../edicion/IndividualEdicion';

describe('Control de componentes de contenido y actividades', () => {
    it("Verificar el renderizado del componente de registro de contenido", () => {
        const componenteContenido= render(<ContenidoRegistro />);
        // Conocer si el componente existe o no
        expect(componenteContenido).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteContenido.getByText("Registro de contenido")).toBeInTheDocument();
        // Conocer la existencia de las indicaciones
        expect(componenteContenido.getByText("Indicaciones")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteContenido.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de contenido registrado
        expect(cancelarRegistro).toHaveAttribute("to", "/");
        // Verificar cierre del modal
        const btnModal = componenteContenido.getByText("Entendido");
        fireEvent.click(btnModal);
        // Verificar que el modal se cierre
        expect(btnModal).not.toBeInTheDocument();
    });
    it("Verificar el renderizado del componente de edición de contenido", () => {
        const edicionContenido= render(<ContenidoEdición />);
        // Conocer si el componente existe o no
        expect(edicionContenido).toBeTruthy();
        // Conocer la existencia del titulo
        expect(edicionContenido.getByText("Edición de contenido")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = edicionContenido.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // tarjeta de contenido
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
    it("Verificar el renderizado del componente de registro de actividad", () => {
        const componenteActi= render(<IndividualRegistro />);
        // Conocer si el componente existe o no
        expect(componenteActi).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteActi.getByText("Registro de Contenido")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteActi.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de actividades registradas
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
    it("Verificar el renderizado del componente de edición de actividad", () => {
        const edicionActividad= render(<IndividualEdición />);
        // Conocer si el componente existe o no
        expect(edicionActividad).toBeTruthy();
        // Conocer la existencia del titulo
        expect(edicionActividad.getByText("Edición de contenido")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = edicionActividad.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // tarjeta de actividad
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
});
*/

/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { SalaRegistro } from './SalaRegistro';
import { SalasEdicion } from '../edicion/SalaEdicion';

describe('Control de componentes de salas', () => {
    it("Verificar el renderizado del componente de registro de sala", () => {
        const componenteSala= render(<SalaRegistro />);
        // Conocer si el componente existe o no
        expect(componenteSala).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteSala.getByText("Registro de Sala")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteSala.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de salas registradas o niveles registrados
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
    it("Verificar el renderizado del componente de edición de sala", () => {
        const compoSalaEdicion= render(<SalasEdicion />);
        // Conocer si el componente existe o no
        expect(compoSalaEdicion).toBeTruthy();
        // Conocer la existencia del titulo
        expect(compoSalaEdicion.getByText("Edición de Sala")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = compoSalaEdicion.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // tarjeta de sala o listado de salas registradas
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
});

*/

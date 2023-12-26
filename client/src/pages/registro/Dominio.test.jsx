/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { DominioRegistro } from './DominioRegistro';
import { DominioEdición } from '../edicion/DominioEdicion';

describe('Control de componentes de dominio', () => {
    it("Verificar el renderizado del componente de registro de dominio", () => {
        const componenteDominio= render(<DominioRegistro />);
        // Conocer si el componente existe o no
        expect(componenteDominio).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteDominio.getByText("Registro de Dominio")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteDominio.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de niveles registrados o dominios registrados
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
    it("Verificar el renderizado del componente de edición de dominio", () => {
        const componenteDominEdi= render(<DominioEdición />);
        // Conocer si el componente existe o no
        expect(componenteDominEdi).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteDominEdi.getByText("Edición de dominio")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteDominEdi.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // tarjeta de dominio
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
});
*/

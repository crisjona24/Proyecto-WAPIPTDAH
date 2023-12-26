/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { PeticionRegistro } from './PeticionRegistro';

describe('Control de componentes de petición', () => {
    it("Verificar el renderizado del componente de registro de petición", () => {
        const componentePeticion= render(<PeticionRegistro />);
        // Conocer si el componente existe o no
        expect(componentePeticion).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componentePeticion.getByText("Registro de Petición")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componentePeticion.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de peticiones registradas
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
});
*/

/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { NivelRegistro } from './NivelRegistro';
import { NivelEdición } from '../edicion/NivelEdicion';

describe('Control de componentes de nivel', () => {
    it("Verificar el renderizado del componente de registro de nivel", () => {
        const componenteNivel= render(<NivelRegistro />);
        // Conocer si el componente existe o no
        expect(componenteNivel).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteNivel.getByText("Registro de Nivel")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteNivel.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de niveles registrados
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
    it("Verificar el renderizado del componente de edición de nivel", () => {
        const componenteNivelEdi= render(<NivelEdición />);
        // Conocer si el componente existe o no
        expect(componenteNivelEdi).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteNivelEdi.getByText("Edición de nivel")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteNivelEdi.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de niveles registrados
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
});
*/
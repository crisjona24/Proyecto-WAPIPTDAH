/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { ResultadoEdicion } from '../edicion/ResultadoEdicion';

describe('Control de componentes de resultado', () => {
    it("Verificar el renderizado del componente de edición de resultado", () => {
        const componenteResult= render(<ResultadoEdicion />);
        // Conocer si el componente existe o no
        expect(componenteResult).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteResult.getByText("Agregar Observación")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteResult.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de resultados registrados
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
});
*/

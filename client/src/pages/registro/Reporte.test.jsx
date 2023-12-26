/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { ReporteEdicion } from '../edicion/ReporteEdicion';

describe('Control de componentes de reportes', () => {
    it("Verificar el renderizado del componente de edición de reporte", () => {
        const componenteReporte= render(<ReporteEdicion />);
        // Conocer si el componente existe o no
        expect(componenteReporte).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteReporte.getByText("Agregar Descripción")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteReporte.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // tarjeta de reporte o listado de los mismos
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
});
*/


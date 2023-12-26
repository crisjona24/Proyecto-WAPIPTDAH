/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { CursoRegistro } from './CursoRegistro';
import { CursoEdicion } from '../edicion/CursoEdicion';

describe('Control de componentes de curso', () => {
    it("Verificar el renderizado del componente de registro de curso", () => {
        const componenteCurso = render(<CursoRegistro />);
        // Conocer si el componente existe o no
        expect(componenteCurso).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteCurso.getByText("Registro de Curso")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = componenteCurso.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de cursos registrados o niveles registrados
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
    it("Verificar el renderizado del componente de edición de curso", () => {
        const compoCursoEdi= render(<CursoEdicion />);
        // Conocer si el componente existe o no
        expect(compoCursoEdi).toBeTruthy();
        // Conocer la existencia del titulo
        expect(compoCursoEdi.getByText("Edición de Curso")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const cancelarRegistro = compoCursoEdi.getByText("Cancelar");
        fireEvent.click(cancelarRegistro);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // tarjeta de curso o listado de cursos
        expect(cancelarRegistro).toHaveAttribute("to", "/");
    });
});

*/

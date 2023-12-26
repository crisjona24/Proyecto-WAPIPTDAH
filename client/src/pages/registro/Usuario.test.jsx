/*
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { UsuarioComunRegistro } from './UsuarioComunRegistro';
import { UsuarioPacienteRegistro } from './UsuarioPacienteRegistro';
import { UsuarioRegistro } from './UsuarioRegistro';

describe('Registro de usuarios por rol', () => {
    it("Verificar el renderizado del componente de registro de usuario común", () => {
        const componenteUC= render(<UsuarioComunRegistro />);
        // Conocer si el componente existe o no
        expect(componenteUC).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteUC.getByText("Registro de usuario")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const botonCancelar = componenteUC.getByText("Cancelar");
        fireEvent.click(botonCancelar);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de inicio
        expect(botonCancelar).toHaveAttribute("to", "/");
    });
    it("Verificar el renderizado del componente de registro de usuario técnico", () => {
        const componenteUT= render(<UsuarioRegistro />);
        // Conocer si el componente existe o no
        expect(componenteUT).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteUT.getByText("Registro de técnico")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const botonCancelar = componenteUT.getByText("Cancelar");
        fireEvent.click(botonCancelar);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de inicio
        expect(botonCancelar).toHaveAttribute("to", "/");
    });
    it("Verificar el renderizado del componente de registro de usuario paciente", () => {
        const componenteUP= render(<UsuarioPacienteRegistro />);
        // Conocer si el componente existe o no
        expect(componenteUP).toBeTruthy();
        // Conocer la existencia del titulo
        expect(componenteUP.getByText("Registro de estudiante")).toBeInTheDocument();
        // Verificar la respuesta al dar click al boton cancelar registro
        const botonCancelar = componenteUP.getByText("Cancelar");
        fireEvent.click(botonCancelar);
        // Verificar que al dar click en el boton de cancelar se redirija a la 
        // pagina de inicio
        expect(botonCancelar).toHaveAttribute("to", "/");
    });
});

*/

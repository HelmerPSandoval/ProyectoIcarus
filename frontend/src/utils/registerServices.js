import {mensajeExito, mensajeError} from "./store";

export async function registrarUsuario (usuarioARegistrar) {
    let rut = usuarioARegistrar.rut;
    let password = usuarioARegistrar.password;
    let last_login = null;
    let nombre = usuarioARegistrar.nombre;
    let apellido = usuarioARegistrar.apellido;
    let email = usuarioARegistrar.email;
    let rol = 2;
    let sexo = usuarioARegistrar.sexo;
    let telefono = usuarioARegistrar.telefono;
    let fecha_nacimiento = usuarioARegistrar.fecha_nacimiento;
    let usuario_activo = true;
    let usuario_administrador = false;
    try {
        const res = await fetch('http://127.0.0.1:8000/api/usuario/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rut,
                password,
                last_login,
                nombre,
                apellido,
                email,
                rol,
                sexo,
                telefono,
                fecha_nacimiento,
                usuario_activo,
                usuario_administrador,
            })
        })
        const datos = await res.json()
        if(datos.Return == 69)
        {            
            mensajeExito.set("Usuario registrado con éxito.");
        }

    } catch (error) {
        mensajeError.set("Ha ocurrido un error durante el registro.");

    }
}
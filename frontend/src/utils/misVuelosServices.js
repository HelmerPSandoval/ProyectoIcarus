import {mensaje_exito, mensaje_error} from "./store";

export async function cancelarReserva (idReservaCancelada, rutUsuario) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/api/reserva/${idReservaCancelada}`, {
            method: 'DELETE',
        })
        mensaje_exito.set("Reserva cancelada con éxito");

    } catch (error) {
        mensaje_error.set("Ha ocurrido un problema durante la cancelación");
    }

    return cargarTabla(rutUsuario);
}

export async function cargarTabla(rutUsuario){  
    let reservas = []
    const response = await fetch('http://127.0.0.1:8000/api/reserva/');
    const reservasJson = await response.json();
    
        reservasJson.forEach(reservaElemento => {
            if (reservaElemento.rut_usuario == rutUsuario) {
                reservas.push(reservaElemento);
            }      
        });
    return reservas;
};

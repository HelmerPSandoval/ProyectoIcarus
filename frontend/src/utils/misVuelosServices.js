import {mensajeExito, mensajeError} from "./store";

export async function cancelarReserva (idReservaCancelada, rutUsuario) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/api/reserva/${idReservaCancelada}`, {
            method: 'DELETE',
        })
        mensajeExito.set("Reserva cancelada con éxito");

    } catch (error) {
        mensajeError.set("Ha ocurrido un problema durante la cancelación");
    }

    return cargarTabla(rutUsuario);
};

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

import {usuario,mensajeExito, mensajeError} from "./store";
export let vuelos_tabla = []
export let estado_app = 1
export let buffer = false

export async function cargarVuelos(){
    let vuelos = [];
    const response = await fetch('http://127.0.0.1:8000/vuelos/');
    const vuelosJson = await response.json();
    
    vuelosJson.forEach(vueloJson => {
        vuelos.push(vueloJson);          
    });

    return vuelos;
};

export async function cargarCiudades(){
    let ciudades = [];
    const response = await fetch('http://127.0.0.1:8000/ciudades/');
    const ciudadesJson = await response.json();
    
    ciudadesJson.forEach(ciudadJson => {
        ciudades.push(ciudadJson);          
    });
    return ciudades;
};

export async function poblarTabla(id_ciudad_origen,id_ciudad_destino){
    let vuelos = await cargarVuelos()
    let ciudades = await cargarCiudades()

    for (let numero_vuelo = 0; numero_vuelo < vuelos.length; numero_vuelo++) {
                  
        if (vuelos[numero_vuelo].id_ciudad_origen == id_ciudad_origen && 
            vuelos[numero_vuelo].id_ciudad_destino == id_ciudad_destino) {
                vuelos_tabla.push(vuelos[numero_vuelo]);
        }
    }
    
    for (let numero_vuelo_t = 0; numero_vuelo_t < vuelos_tabla.length; numero_vuelo_t++) {
           
        for (let numero_ciudad = 0; numero_ciudad < ciudades.length; numero_ciudad++) {
            
            if (vuelos_tabla[numero_vuelo_t].id_ciudad_origen == ciudades[numero_ciudad].id) {
                vuelos_tabla[numero_vuelo_t].nombre_ciudad_origen = ciudades[numero_ciudad].nombre;
            } 
            if (vuelos_tabla[numero_vuelo_t].id_ciudad_destino == ciudades[numero_ciudad].id) {
                vuelos_tabla[numero_vuelo_t].nombre_ciudad_destino = ciudades[numero_ciudad].nombre;
            } 
        }
    }

    return vuelos_tabla
}

export async function registrarReserva(vueloARegistrar, rut_usuario){
    let fecha_reserva = new Date().toLocaleString()
    let valor_reserva = vueloARegistrar.valor_vuelo
    let vuelo = vueloARegistrar.id
    console.log(fecha_reserva,valor_reserva,vuelo,rut_usuario)
    try {
        buffer = true
        const res = await fetch('http://127.0.0.1:8000/api/reserva/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fecha_reserva,
                valor_reserva,
                vuelo,
                rut_usuario,
    
            })
        })
        const datos = await res.json()
        if(datos.Return == 69)
        { 
            buffer = false
            mensajeExito.set("Reserva registrada con éxito.");
            estado_app = 1
        }

    } catch (error) {
        mensajeError.set("Ha ocurrido un error durante el registro.");
        
    }
}

export async function registrarPago(datosTarjeta, rut_usuario){
    let tarjeta_credito = datosTarjeta[0]
    let numero_tarjeta = datosTarjeta[1]
    let fecha_vencimiento = datosTarjeta[2]
    let cvc = datosTarjeta[3]
    try {
        const res = await fetch('http://127.0.0.1:8000/pagos/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tarjeta_credito,
                numero_tarjeta,
                fecha_vencimiento,
                cvc,
                rut_usuario,
                
            })
        })
        const datos = await res.json()
        if(datos.Return == 69)
        { 
            
            mensajeExito.set("Pago registrado.") ;
            
        }

    } catch (error) {
        mensajeError.set("Ha ocurrido un error durante el registro.");
        
    }
}

export function limpiarVuelos(){
    vuelos_tabla = []
};
import {mensajeExito, mensajeError} from "./store";

export async function cargarDropDownCiudades(){
    let ciudades = [];
    const response = await fetch('http://127.0.0.1:8000/ciudades/');
    const ciudadesJson = await response.json();
    
    ciudadesJson.forEach(ciudadElemento => {
        ciudades.push(ciudadElemento);          
    });

    return ciudades;
};

export async function cargarDropDownAviones(){
    let aviones = [];
    const response = await fetch('http://127.0.0.1:8000/aviones/');
    const avionesJson = await response.json();
    
    avionesJson.forEach(avionElemento => {
        aviones.push(avionElemento);          
    });

    return aviones;
};

export async function cargarDropDownVuelos(){
    let vuelos = [];
    const response = await fetch('http://127.0.0.1:8000/vuelos');
    const vuelosJson = await response.json();
    
    vuelosJson.forEach(vueloElemento => {
        vuelos.push(vueloElemento);          
    });

    return vuelos;
};

export async function fetchVueloSeleccionado(idVueloSeleccionado){
    const response = await fetch(`http://127.0.0.1:8000/vuelo/${idVueloSeleccionado}`)
    const vueloSeleccionadoJson = await response.json();
    
    return vueloSeleccionadoJson;
};

export async function registrarCiudad (ciudadARegistrar) {
    let nombre = ciudadARegistrar.nombre;
    let pais = ciudadARegistrar.pais;
    try {
        const res = await fetch('http://127.0.0.1:8000/ciudades/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre,
                pais,
            })
        })
        const datos = await res.json()
        if(datos.Return == 69)
        { 
            mensajeExito.set("Ciudad registrada con éxito.");
        }

    } catch (error) {
        mensajeError.set("Ha ocurrido un error durante el registro.");
    }
};

export async function registrarAvion (avionARegistrar) {
    let modelo = avionARegistrar.modelo;
    let capacidad = avionARegistrar.capacidad;
    try {
        const res = await fetch('http://127.0.0.1:8000/aviones/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                modelo,
                capacidad,
            })
        })
        const datos = await res.json()
        if(datos.Return == 69)
        {            
            mensajeExito.set("Avión registrado con éxito.");
        }

    } catch (error) {
        mensajeError.set("Ha ocurrido un error durante el registro.");
    }
};

export async function editarVuelo (vueloAEditar) {
    let fecha_salida=vueloAEditar.fecha_salida;
	let hora_salida=vueloAEditar.hora_salida;
	let fecha_llegada=vueloAEditar.fecha_llegada;
	let hora_llegada=vueloAEditar.hora_llegada;
    let valor_vuelo=vueloAEditar.valor_vuelo;
	let id_ciudad_origen=vueloAEditar.id_ciudad_origen;
	let id_ciudad_destino=vueloAEditar.id_ciudad_destino;
	let id_avion_asociado=vueloAEditar.id_avion_asociado;
    let id=vueloAEditar.id; 
    console.log("id: ", id);

    try {
        const res = await fetch(`http://127.0.0.1:8000/vuelo/${id}`, {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id,
                fecha_salida,
                hora_salida,
                fecha_llegada,
                hora_llegada,
                valor_vuelo,
                id_ciudad_origen,
                id_ciudad_destino,
                id_avion_asociado,
            })
        })
        const datos = await res.json()
        console.log(datos);
        if(datos.Return == 69)
        {             
            mensajeExito.set("Vuelo editado con éxito.");
        }


    } catch (error) {

        mensajeError.set("Ha ocurrido un error durante el registro.");

    }
};

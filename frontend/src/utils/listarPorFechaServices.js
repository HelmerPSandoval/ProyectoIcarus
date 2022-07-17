export let vuelos_tabla = []
export async function cargarFechasSalida(){
    let fechas_salida = [];
    const response = await fetch('http://127.0.0.1:8000/vuelos/');
    const vuelosJson = await response.json();
    
    vuelosJson.forEach(vueloJson => {
        fechas_salida.push(vueloJson.fecha_salida);          
    });

    return fechas_salida;
};

export async function cargarFechasLlegada(){
    let fechas_llegada = [];
    const response = await fetch('http://127.0.0.1:8000/vuelos/');
    const vuelosJson = await response.json();
    
    vuelosJson.forEach(vueloJson => {
        fechas_llegada.push(vueloJson.fecha_llegada);          
    });

    return fechas_llegada;
};

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

export async function poblarTabla(fecha_salida,fecha_llegada){
    let vuelos = await cargarVuelos()
    let ciudades = await cargarCiudades()

    
    for (let numero_vuelo = 0; numero_vuelo < vuelos.length; numero_vuelo++) {
                  
        if (vuelos[numero_vuelo].fecha_salida == fecha_salida && 
            vuelos[numero_vuelo].fecha_llegada == fecha_llegada) {
                vuelos_tabla.push(vuelos[numero_vuelo]);
                console.log(vuelos_tabla)
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

export function limpiarVuelos(){
    vuelos_tabla = []

};
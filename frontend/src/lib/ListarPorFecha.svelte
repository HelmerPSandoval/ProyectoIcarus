<script>
    import {Tooltip, Alert, Table, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario, mensajeExito, mensajeError} from "../utils/store";
    import { onMount } from "svelte";

	let fechas_salida = []
    let fecha_salida = ''
	let fechas_llegada = []
    let fecha_llegada = ''
    let vuelos = []
    let vuelos_tabla = []
    let ciudades = []

    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/vuelos/');
        const vuelos_json = await response.json();
        
        for(let i=0; i<vuelos_json.length;i++){

            vuelos[i] = vuelos_json[i];
            fechas_salida[i] = vuelos_json[i].fecha_salida;
            fechas_llegada[i] = vuelos_json[i].fecha_llegada;
        }
    })

    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/ciudades/');
        const ciudades_json = await response.json();
        
        for(let i=0; i<ciudades_json.length;i++){
            
            ciudades[i] = ciudades_json[i]
        }
    })

    let poblar_tabla = () => {
        for (let numero_vuelo = 0; numero_vuelo < vuelos.length; numero_vuelo++) {
                  
            if (vuelos[numero_vuelo].fecha_salida == fecha_salida && 
                vuelos[numero_vuelo].fecha_llegada == fecha_llegada) {
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
        
        
    }


    let home = () => {
        $mensajeExito = null;
        $mensajeError = null;
        navigate("/home", {replace:true}); 
    }

    let vaciar_tabla = () => {
        vuelos_tabla = [];
        fecha_salida = ''
        fecha_llegada = ''  
    }

</script>

<Styles />
<div>
    <button type="button" id="boton_home" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
    <Tooltip target="boton_home" placement="right">Volver al inicio</Tooltip>
</div>
<h1>Vuelos Ordenados por Fecha de Salida y Llegada</h1>
<h4>Seleccione una fecha de salida y de llegada</h4>

<main> 
    <br>
    <div class="row mx-auto mt-9 justify-content-between" style="width: 800px;">
        <div class="row mx-auto justify-content-between" style="width: 850px;">
            <div class="col-5">
                <FormGroup floating label="Fecha de salida">
                    <select class="form-select mb-3" aria-label="Default select example" bind:value={fecha_salida} on:change={poblar_tabla} >
                        {#each fechas_salida as fecha_salida}
                        <option>{fecha_salida}</option>                  
                        {/each}                    
                    </select>
                </FormGroup>
            </div>
            <div class="col-5">
                <FormGroup floating label="Fecha de llegada">
                    <select class="form-select mb-3" aria-label="Default select example" bind:value={fecha_llegada} on:change={poblar_tabla} >
                        {#each fechas_llegada as fecha_llegada}
                        <option>{fecha_llegada}</option>                  
                        {/each}   
                    </select>
                </FormGroup>
            </div>
            <div class="col-1">
                <button type="button" id="boton_refrescar" class="btn boton_login mt-2" on:click={vaciar_tabla}><Icon name="arrow-counterclockwise" /></button>
                <Tooltip target="boton_refrescar" placement="right">Refrescar registros</Tooltip>
            </div>
        </div>
        <div class="row mx-auto" style="width: 850px;">
            <div class="col">
                {#if fecha_salida != '' && fecha_llegada != ''}
                    <Table hover bordered>
                        <thead>
                        <tr>
                            <th>Id</th>
                            <th>Ciudad Origen</th>
                            <th>Fecha Salida</th>
                            <th>Ciudad Destino</th>
                            <th>Fecha Llegada</th>
                        </tr>
                        </thead>
                        <tbody>
                            
                            {#each vuelos_tabla as vuelo_tabla}
                                <tr>
                                    <th scope="row">IC {vuelo_tabla.id}</th>
                                    <td>{vuelo_tabla.nombre_ciudad_origen}</td>
                                    <td>{vuelo_tabla.fecha_salida} - {vuelo_tabla.hora_salida}</td>
                                    <td>{vuelo_tabla.nombre_ciudad_destino}</td>
                                    <td>{vuelo_tabla.fecha_llegada} - {vuelo_tabla.hora_llegada}</td>
                                </tr>
                            {/each}
                        
                        </tbody>
                    </Table>
                {/if}
            </div>
        </div>
        
    </div>


</main>
<style>
      
      .boton_icarus {
        background-color: #0b5394;
        color: white;
        position :fixed;
        justify-self: left;
        top: 10px;
        left: 15px;

    }
    .boton_icarus:hover {
    background-color: #0d68ba;
    color: white;
    }

    
    h1 {
        color: #0b5394;
        font-weight: bold;
    }
    h4 {
        color: #0b5394;
        
    }
    .boton_login {
        background-color: #0b5394;
        color: white;
    }
    .boton_login:hover {
    background-color: #0d68ba;
    color: white;
    }
</style>
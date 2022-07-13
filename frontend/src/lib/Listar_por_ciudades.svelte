<script>
    import {Tooltip, Alert, Table, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario, mensaje_exito} from "../utils/store";
    import { onMount } from "svelte";

	let fecha_salida = ''
	let hora_salida = ''
	let fecha_llegada = ''
	let hora_llegada = ''
	let id_ciudad_origen = 0
	let id_ciudad_destino = 0
	let id_avion_asociado = 0
    let id = 0 //id de vuelo
    let vuelos = []
    let ciudades = []
    let vuelos_tabla = []

    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/vuelos/');
        const vuelos_json = await response.json();
        
        for(let i=0; i<vuelos_json.length;i++){

            vuelos[i] = vuelos_json[i];
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
        
        
    }

    let home = () => {
        $mensaje_exito=null;
        navigate("/home", {replace:true}); 
    }

    let vaciar_tabla = () => {
        vuelos_tabla = [];
        id_ciudad_origen = 0;
        id_ciudad_destino = 0;

    }

    
</script>

<Styles />
<div>
    <button type="button" id="boton_home" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
    <Tooltip target="boton_home" placement="right">Volver al inicio</Tooltip>
</div>
<h1>Vuelos Ordenados por Ciudad de Origen y Destino</h1>
<h4>Seleccione una ciudad de origen y de destino</h4>

<main> 
    <br>
    <div class="row mx-auto mt-9 justify-content-between" style="width: 800px;">
        <div class="row mx-auto justify-content-between" style="width: 850px;">
            <div class="col-5">
                <FormGroup floating label="Ciudad de Origen">
                    <select class="form-select mb-3" aria-label="Default select example" bind:value={id_ciudad_origen} on:change={poblar_tabla} >
                        {#each ciudades as ciudad}
                        <option value="{ciudad.id}">[{ciudad.id}] - {ciudad.nombre}</option>                  
                        {/each}                    
                    </select>
                </FormGroup>
            </div>
            <div class="col-5">
                <FormGroup floating label="Ciudad de Destino">
                    <select class="form-select mb-3" aria-label="Default select example" bind:value={id_ciudad_destino} on:change={poblar_tabla} >
                        {#each ciudades as ciudad}
                        <option value="{ciudad.id}">[{ciudad.id}] - {ciudad.nombre} </option>                  
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
                {#if id_ciudad_origen != 0 && id_ciudad_destino != 0}
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

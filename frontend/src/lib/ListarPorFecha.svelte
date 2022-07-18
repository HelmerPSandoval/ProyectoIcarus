<script>
    import {Tooltip, Alert, Table, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { navigate } from "svelte-routing";
    import {usuario, mensajeExito, mensajeError} from "../utils/store";
    import * as listarPorFechaServices from "../utils/listarPorFechaServices";

	let fechas_salida_promise = listarPorFechaServices.cargarFechasSalida()
    let fecha_salida = ''
	let fechas_llegada_promise = listarPorFechaServices.cargarFechasLlegada()
    let fecha_llegada = ''
    let vuelos_tabla_promise

    let home = () => {
        $mensajeExito = null;
        $mensajeError = null;
        listarPorFechaServices.limpiarVuelos()
        navigate("/home", {replace:true}); 
    }

    let vaciar_tabla = () => {
        listarPorFechaServices.limpiarVuelos()
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
                    <select class="form-select mb-3" aria-label="Default select example" bind:value={fecha_salida} >
                        {#await fechas_salida_promise}
                            
                        {:then fechas_salida} 
                            <option selected disabled hidden style='display: none' value=''></option>
                            {#each fechas_salida as fecha_salida}
                                <option>{fecha_salida}</option>                  
                            {/each}                    
                        {/await}
                    </select>
                </FormGroup>
            </div>
            <div class="col-5">
                <FormGroup floating label="Fecha de llegada">
                    <select class="form-select mb-3" aria-label="Default select example" bind:value={fecha_llegada} >
                        {#await fechas_llegada_promise}
                            
                        {:then fechas_llegada}   
                            <option selected disabled hidden style='display: none' value=''></option>  
                            {#each fechas_llegada as fecha_llegada}
                                <option>{fecha_llegada}</option>                  
                            {/each}   
                        {/await}
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
                {#if fecha_salida != '' && fecha_llegada != '' }    
                    {#await  vuelos_tabla_promise = listarPorFechaServices.poblarTabla(fecha_salida,fecha_llegada)}
                    {:then vuelos_tabla}    
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
                    {/await}
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
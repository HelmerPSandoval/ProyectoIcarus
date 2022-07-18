<script>
    import {Spinner, Tooltip, Alert, Table, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { navigate } from "svelte-routing";
    import {usuario, mensajeExito, mensajeError} from "../utils/store";
    import { onMount } from "svelte";
    import * as reservarVueloServices from "../utils/reservarVueloServices";

    //Estado 1
    let datosTarjeta
    let buffer = false
    let estado_app = reservarVueloServices.estado_app
    let ciudades_promise = reservarVueloServices.cargarCiudades()
    let rut_usuario = $usuario.rut
	let id_ciudad_origen = 0
	let id_ciudad_destino = 0
    let vueloARegistrar = {}
    let vuelos_tabla_promise

    //Estado 2
    let tarjeta_credito;
    let numero_tarjeta;
    let numero_tarjeta_dinamico;
    let mes_vencimiento
    let anio_vencimiento
    let fecha_vencimiento = mes_vencimiento+"/"+anio_vencimiento
    let cvc


    let tc_usuario_json; //la tarjeta del usuario activo
    let ya_tiene_pago = false; 
    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/pagos/');
        const pagos = await response.json();
        
        for (let tc = 0; tc < pagos.length; tc++) {
            
            if (pagos[tc].rut_usuario == $usuario.rut) {
                tc_usuario_json = pagos[tc]
                ya_tiene_pago = true 
                tarjeta_credito = tc_usuario_json.tarjeta_credito
                numero_tarjeta = tc_usuario_json.numero_tarjeta
                fecha_vencimiento = tc_usuario_json.fecha_vencimiento
                cvc = tc_usuario_json.cvc

                //cargar datos en imagen tarjeta de credito
                let numero_tarjeta_str = numero_tarjeta.toString();
                numero_tarjeta_dinamico = numero_tarjeta_str.slice(0, 4) + " " + numero_tarjeta_str.slice(4, 8) +" "+
                numero_tarjeta_str.slice(8, 12) + " " + numero_tarjeta_str.slice(12, 16);
                mes_vencimiento = fecha_vencimiento.slice(0,2)
                anio_vencimiento = fecha_vencimiento.slice(3,5)
                break;
            }     
        }  
    })

    async function registrarPago(){
        llevarDatosTarjeta()
        reservarVueloServices.registrarPago(datosTarjeta,rut_usuario)
        ya_tiene_pago = true
    }

    async function registrarReserva() {
        reservarVueloServices.registrarReserva(vueloARegistrar,rut_usuario)
        vueloARegistrar = {}
	}

    async function llevarDatosTarjeta(){
        datosTarjeta = []
        datosTarjeta.push(tarjeta_credito)
        datosTarjeta.push(numero_tarjeta)
        datosTarjeta.push(fecha_vencimiento)
        datosTarjeta.push(cvc)
    }

    async function cambiarEstado (vuelo_json) {
        vueloARegistrar = vuelo_json
        estado_app = 2
	}

    let home = () => {
        reservarVueloServices.limpiarVuelos()
        $mensajeExito=null;
        $mensajeError=null;
        navigate("/home", {replace:true}); 
    }

    let vaciarTabla = () => {
        reservarVueloServices.limpiarVuelos()
        id_ciudad_origen = 0;
        id_ciudad_destino = 0;

    }

    //figura tarjeta de credito
    let update_numero_dinamico = () => {
    
    numero_tarjeta_dinamico = numero_tarjeta.slice(0, 4) + " " + numero_tarjeta.slice(4, 8) +" "+
                                numero_tarjeta.slice(8, 12) + " " + numero_tarjeta.slice(12, 16);
    }
</script>

<Styles />
<div>
    <button type="button" id="boton_home" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
    <Tooltip target="boton_home" placement="right">Volver al inicio</Tooltip>
</div>
<h1>Realizar reserva</h1>
<div class="row mx-auto mt-3" style="display: flex; width: 400px;">     
    {#if $mensajeExito != null} 
            <Alert style="text-align: center;" color="info" dismissible>{$mensajeExito}</Alert>
    {/if}           
    {#if $mensajeError != null} 
            <Alert style="text-align: center;" color="danger" dismissible>{$mensajeError}</Alert>
    {/if}      
</div>
<main> 
    {#if estado_app == 1}
    <h4>Seleccione una ciudad de origen y de destino para desplegar vuelos disponibles</h4>
    <br>
    <div class="row mx-auto mt-9 justify-content-between" style="width: 1000px;">
        <div class="row mx-auto justify-content-between" style="width: 850px;">
            <div class="col-5">
                <FormGroup floating label="Ciudad de Origen">
                    <select class="form-select mb-3" aria-label="Default select example" bind:value={id_ciudad_origen}>
                        {#await ciudades_promise}
                        {:then ciudades}     
                            <option selected disabled hidden style='display: none' value=''></option>
                            {#each ciudades as ciudad}
                            <option value="{ciudad.id}">[{ciudad.id}] - {ciudad.nombre}</option>                  
                            {/each}                    
                        {/await}
                    </select>
                </FormGroup>
            </div>
            <div class="col-5">
                <FormGroup floating label="Ciudad de Destino">
                    <select class="form-select mb-3" aria-label="Default select example" bind:value={id_ciudad_destino}>
                        {#await ciudades_promise}
                        {:then ciudades}
                            <option selected disabled hidden style='display: none' value=''></option>     
                            {#each ciudades as ciudad}
                            <option value="{ciudad.id}">[{ciudad.id}] - {ciudad.nombre}</option>                  
                            {/each}                    
                        {/await}   
                    </select>
                </FormGroup>
            </div>
            <div class="col-1">
                <button type="button" id="boton_refrescar" class="btn boton_login mt-2" on:click={vaciarTabla}><Icon name="arrow-counterclockwise" /></button>
                <Tooltip target="boton_refrescar" placement="right">Refrescar registros</Tooltip>
            </div>
        </div>
        <div class="row mx-auto" style="width: 1000px;">
            <div class="col">
                {#if id_ciudad_origen != 0 && id_ciudad_destino != 0}
                    {#await vuelos_tabla_promise = reservarVueloServices.poblarTabla(id_ciudad_origen, id_ciudad_destino)}
                    {:then vuelos_tabla}      
                        <Table hover bordered>
                            <thead>
                            <tr>
                                <th>Id</th>
                                <th>Ciudad Origen</th>
                                <th>Fecha Salida</th>
                                <th>Ciudad Destino</th>
                                <th>Fecha Llegada</th>
                                <th>Valor vuelo</th>
                                <th>Reservar</th>
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
                                        <td>{vuelo_tabla.valor_vuelo}</td>
                                        <td><button type="button" class="btn btn-success" on:click={() => cambiarEstado(vuelo_tabla)}><Icon name="cart-plus" /></button></td>
                                    </tr>
                                {/each}
                            
                            </tbody>
                        </Table>
                    {/await}
                {/if}
            </div>
        </div>
        
    </div>

    {:else if estado_app == 2}
    <h4>Ingrese los datos de su tarjeta de crédito</h4>
    <br>
    <div class="container">
        <div class="row" style="justify-content:center;">

            <div class= "col-8 datos" >
                <Form>
                    <div>
                        <FormGroup floating label="Tarjeta de crédito">
                            <Input class="h3 mb-3 fw-normal" bind:value={tarjeta_credito}/>
                        </FormGroup>
                    </div>
                
                    <div>
                        <FormGroup floating label="Número de tarjeta">
                            <Input class="h3 mb-3 fw-normal" bind:value={numero_tarjeta} on:keyup={update_numero_dinamico}/>
                        </FormGroup>
                    </div>
                    <div class="row">
                        
                        <div class="col">
                            <FormGroup floating label="Mes de vencimiento">
                                <Input class="h3 mb-3 fw-normal" bind:value={mes_vencimiento}/>
                            </FormGroup>
                        </div>
                        
                        <div class="col">
                            <FormGroup floating label="Año de vencimiento">
                                <Input class="h3 mb-3 fw-normal" bind:value={anio_vencimiento}/>
                            </FormGroup>
                        
                        </div>
                    </div>
                    <div>
                        <FormGroup floating label="CVC">
                            <Input class="h3 mb-3 fw-normal" type="password" bind:value={cvc} />
                        </FormGroup>
                    </div>
        
                    <div>
                        <div class="row" style="justify-content: center;">
                            {#if reservarVueloServices.buffer == false} 
                                {#if ya_tiene_pago == false}        
                                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={registrarPago}>Agregar Tarjeta</button>
                                {:else if ya_tiene_pago == true}
                                <button type="button" class="h3 mt-3 fw-normal btn btn-success" on:click={registrarReserva}>Confirmar Reserva</button>     
                                {/if}
                            {:else if reservarVueloServices.buffer == true}
                            <Spinner color="success" />
                            {/if}
                        </div>
                    </div>
                </Form>
            </div>
            <div class="col-4 tc">
                <div class="container-tc">
                    <Image fluid alt="Icarus Airline" class="tc" src="images/tc_en_blanco.png" />
                    
                    <div class="numeros">{numero_tarjeta_dinamico}</div>
                    
                    <div class="fecha">{mes_vencimiento}/{anio_vencimiento}</div>
                    
                </div>
            </div>
        </div>
    </div>

    {/if}
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

    .tc {
        height: 10px;
        margin-left: 50px;
        margin-top: 30px;
    }

    .datos{
        max-width: 500px;
        margin-left: 50px;
        
    }

    .numeros{
        
        position: absolute;
        bottom: 90px;
        right: 100px;
        color: white;
        
        font-family: "Monaco", monospace;
        font-size: x-large;
    }
    .fecha{
        position: absolute;
        bottom: 55px;
        right: 200px;
        color: white;
        
        font-family: "Monaco", monospace;
        font-size: large;
    }
    .container-tc{
        position: relative;
    }
</style>

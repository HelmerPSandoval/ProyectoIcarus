<script>
    import {Spinner, Tooltip, Alert, Table, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario, mensaje_exito, mensaje_error} from "../utils/store";
    import { onMount } from "svelte";

    let vuelo
    let fecha_reserva
    let valor_reserva
    let estado_app = 1
    let rut_usuario = $usuario.rut
	let id_ciudad_origen = 0
	let id_ciudad_destino = 0
    let id = 0 //id de vuelo
    let vuelos = []
    let ciudades = []
    let vuelos_tabla = []

    let buffer = false;
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
    
    async function goto_m_pago (vuelo_json) {
        vuelo = vuelo_json.id
        fecha_reserva= new Date().toLocaleString()
        valor_reserva = vuelo_json.valor_vuelo
        estado_app = 2
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

    //Estado 2
    let tarjeta_credito;
    let numero_tarjeta;
    let numero_tarjeta_dinamico;
    let mes_vencimiento
    let anio_vencimiento
    let fecha_vencimiento = mes_vencimiento+"/"+anio_vencimiento
    let cvc
    //figura tarjeta de credito
    let update_numero_dinamico = () => {
        
        numero_tarjeta_dinamico = numero_tarjeta.slice(0, 4) + " " + numero_tarjeta.slice(4, 8) +" "+
                                  numero_tarjeta.slice(8, 12) + " " + numero_tarjeta.slice(12, 16);
    }

    let tc_usuario_json; //la tarjeta del usuario activo
    let ya_tiene_pago = false; 
    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/pagos/');
        const pagos = await response.json();
        
        for (let tc = 0; tc < pagos.length; tc++) {
            
            if (pagos[tc].rut_usuario == $usuario.rut) {
                tc_usuario_json = pagos[tc]
                ya_tiene_pago = true; 

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

    let result;
    
    async function registrar_pago() {
        try {
            fecha_vencimiento = mes_vencimiento+"/"+anio_vencimiento

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
            result = JSON.stringify(datos);
            if(datos.Return == 69)
            { 
                
                $mensaje_exito = "Pago registrado.";
                ya_tiene_pago = true;
                
            }

        } catch (error) {
            $mensaje_error = "Ha ocurrido un error durante el registro.";
            
        }
        
	}

    async function registrar_reserva() {
        try {
            buffer = true;
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
            result = JSON.stringify(datos);
            if(datos.Return == 69)
            { 
                buffer = false;
                $mensaje_exito = "Reserva registrada con éxito.";
                estado_app = 1
            }

        } catch (error) {
            $mensaje_error = "Ha ocurrido un error durante el registro.";
            
        }
        
	}
</script>

<Styles />
<div>
    <button type="button" id="boton_home" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
    <Tooltip target="boton_home" placement="right">Volver al inicio</Tooltip>
</div>
<h1>Realizar reserva</h1>
{#if $mensaje_exito != null} 
    <div class="mt-1" style="margin-left: 400px; margin-right: 400px;">
        <Alert style="text-align: center;" color="info" dismissible>{$mensaje_exito}</Alert>
    </div>
{/if}

{#if $mensaje_error != null} 
    <div class="mt-1" style="margin-left: 400px; margin-right: 400px;">
        <Alert style="text-align: center;" color="danger" dismissible>{$mensaje_error}</Alert>
    </div>
{/if}
<main> 
    {#if estado_app == 1}
    <h4>Seleccione una ciudad de origen y de destino para desplegar vuelos disponibles</h4>
    <br>
    <div class="row mx-auto mt-9 justify-content-between" style="width: 1000px;">
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
        <div class="row mx-auto" style="width: 1000px;">
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
                                    <td><button type="button" class="btn btn-success" on:click={() => goto_m_pago(vuelo_tabla)}><Icon name="cart-plus" /></button></td>
                                </tr>
                            {/each}
                        
                        </tbody>
                    </Table>
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
                            {#if buffer == false} 
                                {#if ya_tiene_pago == false}        
                                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={registrar_pago}>Agregar Tarjeta</button>
                                {:else if ya_tiene_pago == true}
                                <button type="button" class="h3 mt-3 fw-normal btn btn-success" on:click={registrar_reserva}>Confirmar Reserva</button>     
                                {/if}
                            {:else if buffer == true}
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

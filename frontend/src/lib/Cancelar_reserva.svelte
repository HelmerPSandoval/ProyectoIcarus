<script>
    import {Tooltip, Alert, Table, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario, mensaje_exito, mensaje_error} from "../utils/store";
    import { onMount } from "svelte";

    let aux = 0
    let vuelo
    let fecha_reserva
    let valor_reserva
    let rut_usuario = $usuario.rut
    let id = 0 //id de vuelo
    let reservas = []

    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/api/reserva/');
        const reservas_json = await response.json();
        
        for(let i=0; i<reservas_json.length;i++){

            reservas[i] = reservas_json[i];
        }
    })

    async function cancelar_reserva (reserva) {
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/reserva/${reserva}`, {
                method: 'DELETE',
            })
            const datos = await res.json()

            $mensaje_exito="Reserva cancelada con éxito";
            

        } catch (error) {
            $mensaje_error="Ha ocurrido un problema durante la cancelación";
        }
        refrescar_tabla()
        
	}


    async function refrescar_tabla(){
        reservas = []
        const response = await fetch('http://127.0.0.1:8000/api/reserva/');
        const reservas_json = await response.json();
        
        for(let i=0; i<reservas_json.length;i++){

            reservas[i] = reservas_json[i];
        }
    }

    let home = () => {
        $mensaje_exito=null;
        $mensaje_error=null;
        navigate("/home", {replace:true}); 
    }

</script>
<Styles />
<div>
    <button type="button" id="boton_home" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
    <Tooltip target="boton_home" placement="right">Volver al inicio</Tooltip>
</div>
<h1>Mis vuelos</h1>
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
    <div class="form-signin">
        <Table hover bordered>
            <thead>
            <tr>
                <th>Id</th>
                <th>Fecha Reserva</th>
                <th>Valor vuelo</th>
                <th>Cancelar</th>
            </tr>
            </thead>
            <tbody>
                {#each reservas as reserva}
                    {#if reserva.rut_usuario == rut_usuario} 
                        <tr>
                            <th scope="row">IC {reserva.id}</th>
                            <td>{(reserva.fecha_reserva).replace("T"," ").replace("Z","")}</td>
                            <td>{reserva.valor_reserva}</td>
                            <td><button type="button" class="btn btn-danger"  on:click={() => cancelar_reserva(reserva.id)}><Icon name="x-circle" /></button></td>
                        </tr>
                    {/if}
                {/each}     
            </tbody>
        </Table>
    </div>
</main>

<style>

    .form-signin {
    width: 100%;
    max-width: 1060px;
    padding: 15px;
    margin: auto;
    }
    
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

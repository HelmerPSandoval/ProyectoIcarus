<script>
    import { Alert, Label, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario, mensaje} from "../utils/store";
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
    
    console.log("usuario:",$usuario);
    console.log("mensaje:",$mensaje);
    //llenar dropdown id de vuelo
    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/vuelos');
        const vuelos_json = await response.json();
        
        for(let i=0; i<vuelos_json.length;i++){

            vuelos[i] = vuelos_json[i].id
        }
    })


    //llenar datos del vuelo luego de seleccionar un id de vuelo en el dropdown
    function llenar_datos () {
                
        fetch(`http://127.0.0.1:8000/vuelo/${id}`)
        .then( res => res.json())
        .then(data => {
            fecha_salida = data.fecha_salida;
            hora_salida = data.hora_salida;
            fecha_llegada = data.fecha_llegada;
            hora_llegada = data.hora_llegada;
            hora_salida = data.hora_salida;
            id_ciudad_origen = data.id_ciudad_origen;
            id_ciudad_destino = data.id_ciudad_destino;
            id_avion_asociado = data.id_avion_asociado;

        })
    }

	let result = null

    async function editar_vuelo () {
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
                    id_ciudad_origen,
                    id_ciudad_destino,
                    id_avion_asociado,
                })
            })
            const datos = await res.json()
            result = JSON.stringify(datos);
            //console.log(datos)

            $mensaje="Vuelo editado con éxito.";
            

        } catch (error) {
            
        }
	}

    let home = () => {
        $mensaje=null;
        navigate("/home", {replace:true}); 
    }
    let ver_id_vuelo = () =>console.log(id);

    
</script>

<Styles />
<button type="button" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
<h1>Editar vuelo</h1>
<h4>Ingrese la información del vuelo</h4>
{#if $mensaje != null} 
    <div class="mt-1" style="margin-left: 400px; margin-right: 400px;">
        <Alert color="info" dismissible>{$mensaje}</Alert>
    </div>
{/if}
<main class="form-signin"> 
    
    <Form>
        <div>
            <FormGroup floating label="Vuelo">
            <select class="form-select mb-3" aria-label="Default select example" bind:value={id} on:change={llenar_datos}>
                {#each vuelos as _vuelo}
                <option value="{_vuelo}">{_vuelo}</option>                  
                {/each}
                
              </select>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Fecha Salida">
                <Input class="h3 mb-3 fw-normal" type="date" bind:value={fecha_salida}/>
            </FormGroup>
        </div>
        
        <div>
            <FormGroup floating label="Hora Salida">
                <Input class="h3 mb-3 fw-normal" type="time" bind:value={hora_salida}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Fecha Llegada">
                <Input class="h3 mb-3 fw-normal" type="date" bind:value={fecha_llegada}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Hora Llegada">
                <Input class="h3 mb-3 fw-normal" type="time" bind:value={hora_llegada}/>
            </FormGroup>
        </div>

        <div class="form-floating">
            <FormGroup floating label="Id Ciudad Origen">
                <Input class="h3 mb-3 fw-normal" bind:value={id_ciudad_origen} />
            </FormGroup>
        </div>  
        
        <div class="form-floating">
            <FormGroup floating label="Id Ciudad Destino">
                <Input class="h3 mb-3 fw-normal" bind:value={id_ciudad_destino} />
            </FormGroup>
        </div>  

        <div>
            <FormGroup floating label="Id Avión">
                <Input class="h3 mb-3 fw-normal" bind:value={id_avion_asociado}/>
            </FormGroup>
        </div>

        <div>
            <div class="row">
                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={editar_vuelo}>Editar Vuelo</button>
            </div>
        </div>
        
    </Form>


</main>
<style>
    

    .form-signin {
        width: 100%;
        max-width: 330px;
        padding: 15px;
        margin: auto;
    }


    .form-signin .form-floating:focus-within {
    z-index: 2;
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

      .boton_login {
        background-color: #0b5394;
        color: white;
      }
      .boton_login:hover {
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
</style>

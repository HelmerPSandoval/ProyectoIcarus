<script>
    import { Label, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario} from "../utils/store";
    import { onMount } from "svelte";

	let fecha_salida = '2022-10-11'
	let hora_salida = '00:00:00'
	let fecha_llegada = '2022-10-12'
	let hora_llegada = '00:00:00'
	let id_ciudad_origen = 2 
	let id__ciudad_destino = 1
	let id_avion_asociado = 1

    
    
    
	let result = null
    
    let error_ = false;

    async function registrar_vuelo () {
        try {
            const res = await fetch('http://127.0.0.1:8000/vuelos/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    fecha_salida,
                    hora_salida,
                    fecha_llegada,
                    hora_llegada,
                    id_ciudad_origen,
                    id__ciudad_destino,
                    id_avion_asociado,
                })
            })
            const datos = await res.json()
            result = JSON.stringify(datos);
            console.log(result)

        } catch (error) {
            
        }
	}

    
    // fetch("http://127.0.0.1:8000/vuelos/")
    // .then( res => res.json())
    // .then(data => {
    //     console.log(data)
    // })

    let inicio = () => navigate("/", {replace:true});
;

    
</script>

<Styles />
<button type="button" class="h3 mt-3 fw-normal btn boton_icarus" on:click={inicio}><Icon name="house-door-fill" /></button>

<br>
<Image alt="Icarus Airline" src="images/IcarusAirline.png" />
<main class="form-signin"> 
    
    <Form>
        <div>
            <FormGroup floating label="Fecha Salida">
                <Input class="h3 mb-3 fw-normal" type="text" bind:value={fecha_salida}/>
            </FormGroup>
        </div>
        
        <div>
            <FormGroup floating label="Hora Salida">
                <Input class="h3 mb-3 fw-normal" type="text" bind:value={hora_salida}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Fecha Llegada">
                <Input class="h3 mb-3 fw-normal" type="text" bind:value={fecha_llegada}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Hora Llegada">
                <Input class="h3 mb-3 fw-normal" type="text" bind:value={hora_llegada}/>
            </FormGroup>
        </div>

        <div class="form-floating">
            <FormGroup floating label="Id Ciudad Origen">
                <Input class="h3 mb-3 fw-normal" bind:value={id_ciudad_origen} />
            </FormGroup>
        </div>  
        
        <div class="form-floating">
            <FormGroup floating label="Id Ciudad Destino">
                <Input class="h3 mb-3 fw-normal" bind:value={id__ciudad_destino} />
            </FormGroup>
        </div>  

        <div>
            <FormGroup floating label="Id Avión">
                <Input class="h3 mb-3 fw-normal" bind:value={id_avion_asociado}/>
            </FormGroup>
        </div>

        <div>
            <div class="row">
                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={registrar_vuelo}>Registrar Vuelo</button>
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

  </style>

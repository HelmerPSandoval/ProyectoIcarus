<script>
    import { Label, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario} from "../utils/store";

	let email = 'mandarino@maderasrafa.cl'

    let last_login = null
    let usuario_activo = true
    let usuario_administrador = false
    
    
    
	let result = null
    
    let error_ = false;

    async function solicitar_password () {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/usuario/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email,
                })
            })
            const datos = await res.json()
            result = JSON.stringify(datos);

            navigate("/", {replace:true});

        } catch (error) {
            
        }
	}

    // let register = () => navigate("/home", {replace:true});
;

    
</script>

<Image alt="Icarus Airline" src="images/IcarusAirline.png" />
<main class="form-signin"> 
    
    <Form> 
        <div class="form-floating">
            <FormGroup floating label="Email">
                <Input class="h3 mb-3 fw-normal" bind:value={email} />
            </FormGroup>
        </div> 

        <div>
            <div class="row">
                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={solicitar_password}>Solicitar Contraseña</button>
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

    .boton_login {
        background-color: #0b5394;
        color: white;
      }
      .boton_login:hover {
        background-color: #0d68ba;
        color: white;
      }

   

  </style>

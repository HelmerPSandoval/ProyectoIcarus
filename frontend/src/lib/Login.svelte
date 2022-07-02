<script>
    import { Alert, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario, mensaje} from "../utils/store";

	let username = 'mandarino@maderasrafa.cl'
	let password = '123'
	let result = null
    console.log($mensaje)
    let error_ = false;

    async function login () {
        try {
            const res = await fetch('http://127.0.0.1:8000', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    password
                })
            })
            const datos = await res.json()
            result = JSON.stringify(datos);
            if(datos.user.rol != null)
            {
                $usuario = datos.user;
                $mensaje=null;
                navigate("/home", {replace:true});
            }else{
                error_ = true;
            }
        } catch (error) {
            
        }
	}

    let register = () => navigate("/register", {replace:true});
;

    
</script>

<Image alt="Icarus Airline" src="images/IcarusAirline.png" />
{#if $mensaje != null} 
    <div style="margin-left: 400px; margin-right: 400px;">
        <Alert color="info" dismissible>{$mensaje}</Alert>
    </div>
{/if}
<main class="form-signin"> 
    
    <Form>
        <div class="form-floating">
            <FormGroup floating label="Email">
                <Input class="h3 mb-3 fw-normal" bind:value={username} />
            </FormGroup>
        </div>
        
        <div>
            <FormGroup floating label="Contraseña">
                <Input class="h3 mb-3 fw-normal" type="password" bind:value={password}/>
                <a href="/reset_password"> ¿olvidó su contraseña?</a>
            </FormGroup>
        </div>
        
        <div>
            <div class="row">

                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={login}>Iniciar sesión</button>
                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={register}>Registrarse</button>
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

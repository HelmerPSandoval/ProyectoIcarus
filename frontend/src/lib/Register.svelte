<script>
    import { Label, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario} from "../utils/store";

	let rut = '199784242'
	let password = '123'
	let nombre = 'mandarino'
	let apellido = 'wolfgang'
	let email = 'mandarino@maderasrafa.cl'
	let rol = '1'
	let sexo = 'masculino'
	let telefono = '123456789'
	let fecha_nacimiento = '12-11-1998'

    let last_login = null
    let usuario_activo = true
    let usuario_administrador = false
    
    
    
	let result = null
    
    let error_ = false;

    async function registrar_usuario () {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/usuario/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    rut,
                    password,
                    last_login,
                    nombre,
                    apellido,
                    email,
                    rol,
                    sexo,
                    telefono,
                    fecha_nacimiento,
                    usuario_activo,
                    usuario_administrador,
                })
            })
            const datos = await res.json()
            result = JSON.stringify(datos);
            console.log(datos)
            if(!datos.email && !datos.rut && !datos.nombre)
            { 
                navigate("/", {replace:true});
            }else{
                error_ = true;
            }

        } catch (error) {
            
        }
	}

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
            <FormGroup floating label="Rut">
                <Input class="h3 mb-3 fw-normal" bind:value={rut}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Contraseña">
                <Input class="h3 mb-3 fw-normal" bind:value={password}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Nombre">
                <Input class="h3 mb-3 fw-normal" bind:value={nombre}/>
            </FormGroup>
        </div>

        <div class="form-floating">
            <FormGroup floating label="Apellido">
                <Input class="h3 mb-3 fw-normal" bind:value={apellido} />
            </FormGroup>
        </div>  
        
        <div class="form-floating">
            <FormGroup floating label="Email">
                <Input class="h3 mb-3 fw-normal" bind:value={email} />
            </FormGroup>
        </div> 

        <div class="form-floating">
            <FormGroup floating label="Sexo">
                <Input class="h3 mb-3 fw-normal" bind:value={sexo} />
            </FormGroup>
        </div>

        <div class="form-floating">
            <FormGroup floating label="Teléfono">
                <Input class="h3 mb-3 fw-normal" bind:value={telefono} />
            </FormGroup>
        </div>
        
        <div class="form-floating">
            <FormGroup floating label="Fecha de nacimiento">
                <Input  type="date" name="date" class="h3 mb-3 fw-normal" bind:value={fecha_nacimiento} />
            </FormGroup>
            
        </div>

        <div>
            <div class="row">
                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={registrar_usuario}>Registrar Usuario</button>
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

<script>
    import {Alert, Styles, Icon, Input, Form, FormGroup, Image  } from 'sveltestrap';
    import { navigate } from "svelte-routing";
    import {registrarUsuario} from "../utils/registerServices";
    import {usuario, mensajeExito, mensajeError} from "../utils/store";

    let usuarioARegistrar = {};

    let inicio = () => {
        $mensajeExito=null;
        $mensajeError=null;
        navigate("/", {replace:true});

    }
;

    
</script>

<Styles />
<button type="button" class="h3 mt-3 fw-normal btn boton_icarus" on:click={inicio}><Icon name="house-door-fill" /></button>

<br>
<Image alt="Icarus Airline" src="images/IcarusAirline.png" />
<div class="row mx-auto mt-3" style="display: flex; width: 400px;">     
    {#if $mensajeExito != null} 
            <Alert style="text-align: center;" color="info" dismissible>{$mensajeExito}</Alert>
    {/if}           
    {#if $mensajeError != null} 
            <Alert style="text-align: center;" color="danger" dismissible>{$mensajeError}</Alert>
    {/if}      
</div>
<main class="form-signin"> 
    
    <Form>
        <div>
            <FormGroup floating label="Rut">
                <Input class="h3 mb-3 fw-normal" bind:value={usuarioARegistrar.rut}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Contraseña">
                <Input class="h3 mb-3 fw-normal" type="password" bind:value={usuarioARegistrar.password}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Nombre">
                <Input class="h3 mb-3 fw-normal" bind:value={usuarioARegistrar.nombre}/>
            </FormGroup>
        </div>

        <div class="form-floating">
            <FormGroup floating label="Apellido">
                <Input class="h3 mb-3 fw-normal" bind:value={usuarioARegistrar.apellido} />
            </FormGroup>
        </div>  
        
        <div class="form-floating">
            <FormGroup floating label="Email">
                <Input class="h3 mb-3 fw-normal" bind:value={usuarioARegistrar.email} />
            </FormGroup>
        </div> 

        <div>
            <FormGroup floating label="Sexo">
            <select class="form-select mb-3" aria-label="Default select example" bind:value={usuarioARegistrar.sexo}>
                <option value="hombre">hombre</option>
                <option value="mujer">mujer</option>
                <option value="otro">otro</option>
              </select>
            </FormGroup>
        </div>

        <div class="form-floating">
            <FormGroup floating label="Teléfono">
                <Input class="h3 mb-3 fw-normal" bind:value={usuarioARegistrar.telefono} />
            </FormGroup>
        </div>
        
        <div class="form-floating">
            <FormGroup floating label="Fecha de nacimiento">
                <Input  type="date" name="date" class="h3 mb-3 fw-normal" bind:value={usuarioARegistrar.fecha_nacimiento} />
            </FormGroup>
            
        </div>

        <div>
            <div class="row">
                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={() => registrarUsuario(usuarioARegistrar)}>Registrar Usuario</button>
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

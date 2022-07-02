<script>
    import { Tooltip, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { navigate } from "svelte-routing";
    import {usuario, mensaje} from "../utils/store";
    import { writable } from "svelte/store";
    import { onMount } from 'svelte';


    console.log("usuario:",$usuario);
    console.log("mensaje:",$mensaje);

    onMount(async () => {
		
        if ($usuario == null){
            navigate("/", {replace:true});
            $mensaje = "Se ha cerrado la sesión de manera inesperada, por favor evite refrescar la página."
        }
	});
	
    function logout () {          
        $usuario = writable(null);
        navigate("/", {replace:true}); 
        $mensaje = null;        
	}

    let goto_r_vuelo = () => navigate("/registrar_vuelo", {replace:true});
    let goto_e_vuelo = () => navigate("/editar_vuelo", {replace:true});

    
</script>

<Image fluid alt="Icarus Airline" src="images/IcarusAirline.png"/>
<br>
<Styles />
<div>
    <button type="button" id="btn-logout" class="h3 mt-3 fw-normal btn boton_icarus" 
    on:click={logout}><Icon name="door-open-fill" />
    </button>
    <Tooltip target="btn-logout" placement="right">Cerrar Sesión</Tooltip>
</div>

<main > 
    <div class="container">
        <div class="row mx-auto" style="width: 600px;">
            <div class="row mx-3 justify-content-center">
                <div class="col-md-7 card form-izq ml-3">
                    <h4 class="text-center">
                        {#if $usuario != null}    
                            {#if $usuario.rol==1}
                            Funciones Admin
                            {:else}                
                            Funciones Cliente
                            {/if}
                        
                        {/if}
                    </h4>
                </div>
            </div>
        </div>
        <div class="row mx-auto" style="width: 600px;">
            <div class="col">
                <div class="row justify-content-center mt-2">
                            
                    <div class="row justify-content-evenly mt-3 mx-auto">
                        <div class="col-12">
            
                            <div class="list-group justify-content-left">
                                {#if $usuario != null} 
                                    {#if $usuario.rol==1}
                                    <Button type="button" on:click={goto_r_vuelo}
                                        class="list-group-item list-group-item-action">
                                        <div class="d-flex w-100 justify-content-between">
                                            <h5 class="mb-1">Agregar Nuevo Vuelo</h5>
                                        </div>
                                        <p class="mb-1">Permite a un usuario con derechos de administrador crear una nueva ruta de vuelos.</p>
                                    </Button>
                                    <Button type="button" on:click={goto_e_vuelo} 
                                        class="list-group-item list-group-item-action">
                                        <div class="d-flex w-100 justify-content-between">
                                            <h5 class="mb-1">Editar Vuelo</h5>
                                        </div>
                                        <p class="mb-1">Permite a un usuario con derechos de administrador editar una ruta de vuelos existente.</p>
                                    </Button>
                                    {/if}
                                    
                                {/if}
                                <Button class="list-group-item list-group-item-action">
                                    <div class="d-flex w-100 justify-content-left">
                                        <h5 class="mb-1">Reservar Vuelo</h5>
                                    </div>
                                    <p class="mb-1">Ver vuelos disponibles en el sistema y crear una reservación de vuelo.</p>
                                </Button>
                                <Button class="list-group-item list-group-item-action">
                                    <div class="d-flex w-100 justify-content-left">
                                        <h5 class="mb-1">Listar Vuelos por Ciudad </h5>
                                    </div>
                                    <p class="mb-1">Listar todos los vuelos disponibles para una ciudad específica y un destino particular.</p>
                                </Button>
                                <Button class="list-group-item list-group-item-action">
                                    <div class="d-flex w-100 justify-content-left">
                                        <h5 class="mb-1">Listar Vuelos por Fecha </h5>
                                    </div>
                                    <p class="mb-1">Listar todos los vuelos disponibles en una fecha en particular desde una ciudad hacia un destino.</p>
                                </Button>
                                
                            </div>
                        </div>
                    </div>
            
                    
                </div>

            </div>
        </div>
    </div>


</main>
<style>   
    div {
    text-align: justify;
    text-justify: inter-word;
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
    
  </style>

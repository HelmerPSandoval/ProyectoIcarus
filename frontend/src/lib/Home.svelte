<script>
    import { Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario} from "../utils/store";
    import { writable } from "svelte/store";


	
    function logout () {
           
        $usuario = writable(null);
        navigate("/", {replace:true});
          
	}

    let goto_r_vuelo = () => navigate("/registrar_vuelo", {replace:true});
    let goto_e_vuelo = () => navigate("/editar_vuelo", {replace:true});

    
</script>

<Image fluid alt="Icarus Airline" src="images/IcarusAirline.png" />
<main > 
    
    <div class="row justify-content-center mt-2">
        <div class="col-8 card p-3 bg-light mt-3 col-form-izq">
            <div class="row mx-3 justify-content-center">
                <div class="col-md-7 card form-izq ml-3">
                    <h4 class="text-center">
                        <svg class="bi me-2" width="16" height="16">
                            <use xlink:href="#inventario" />
                        </svg>
                        {#if $usuario.rol==1}
                        Funciones Admin
                        {:else}                
                        Funciones Cliente
                        {/if}
                    </h4>
                </div>
            </div>
            <div class="row justify-content-evenly mt-3 mx-auto">
                <div class="col-12">

                    <div class="list-group justify-content-left">
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
                        <Button class="list-group-item list-group-item-action" on:click={logout}>
                            <div class="d-flex w-100 justify-content-left">
                                <h5 class="mb-1">Logout </h5>
                            </div>
                            <p class="mb-1">Cerrar Sesión.</p>
                        </Button>
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
  </style>

<script>
    import { Alert, Label, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Modal, ModalBody, ModalHeader, ModalFooter  } from 'sveltestrap';
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

    //Rellenar dropdowns de ciudades y avión
    let ciudades = []
    let aviones = []

    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/ciudades/');
        const ciudades_json = await response.json();
        
        for(let i=0; i<ciudades_json.length;i++){
            
            ciudades[i] = ciudades_json[i]
        }
    })
    onMount(async () => {
        const response = await fetch('http://127.0.0.1:8000/aviones/');
        const aviones_json = await response.json();
        
        for(let i=0; i<aviones_json.length;i++){
            
            aviones[i] = aviones_json[i]
        }
    })
    
	let result = null
    
    let error_ = false;
    console.log("usuario:",$usuario);
    console.log("mensaje:",$mensaje);

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
                    id_ciudad_destino,
                    id_avion_asociado,
                })
            })
            const datos = await res.json()
            result = JSON.stringify(datos);
            console.log(result)
            if(datos.Return == 69)
            { 
                
                $mensaje = "Vuelo registrado con éxito.";
            }else{
                error_ = true;
            }

        } catch (error) {
            
        }
	}

    let home = () => {
        $mensaje=null;
        navigate("/home", {replace:true}); 
    }
    
    //logica de Modal Ciudad
    let open = false;
    const toggle = () => {
        size = undefined;
        open = !open;
    };
    //logica de Modal Avion
    let size = 'sm';
    let open_a = false;

    const toggleSm = () => {
        open_a = !open_a;
    };
    
</script>

<Styles />
<button type="button" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
<h1>Registrar nuevo vuelo</h1>
<h4>Ingrese la información del vuelo</h4>
{#if $mensaje != null} 
    <div class="mt-1" style="margin-left: 400px; margin-right: 400px;">
        <Alert color="info" dismissible>{$mensaje}</Alert>
    </div>
{/if}
<main > 
    <div class="container">
        <div class="row mx-auto mt-4" style="width: 300px;">
            <div class="col">

                <Form>
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
                        <div class="row d-flex justify-content-between">
                            <div class="col-9">
                                <div>
                                    <FormGroup floating label="Ciudad Origen">
                                    <select class="form-select mb-3" aria-label="Default select example" bind:value={id_ciudad_origen}>
                                        {#each ciudades as ciudad}
                                        <option value="{ciudad.id}">[{ciudad.id}] - {ciudad.nombre}</option>                  
                                        {/each}
                                        
                                    </select>
                                    </FormGroup>
                                </div>
                            </div>
                            <div class="col">
                                <Modal isOpen={open} backdrop="static" {toggle}>
                                    <ModalHeader>Agregar Ciudad</ModalHeader>
                                    <ModalBody>
                                      Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                                      tempor incididunt ut labore et dolore magna aliqua.
                                    </ModalBody>
                                    <ModalFooter>
                                        <button type="button" class="btn boton_login" on:click={toggle}>Agregar</button>
                                        <button type="button" class="btn btn-secondary" on:click={toggle}>Cancelar</button>
                                    </ModalFooter>
                                </Modal>
                                <button type="button" class="btn boton_login mt-2 offset-md-2" on:click={toggle}><Icon name="plus" /></button>
                            </div>
                        </div>
                    </div>  
                    
                    <div class="form-floating">
                        <div class="row d-flex justify-content-between">
            
                            <div class="col-9">
                                <FormGroup floating label="Ciudad Destino">
                                    <select class="form-select mb-3" aria-label="Default select example" bind:value={id_ciudad_destino}>
                                        {#each ciudades as ciudad}
                                        <option value="{ciudad.id}">[{ciudad.id}] - {ciudad.nombre}</option>                  
                                        {/each}
                                    </select>
                                </FormGroup>
                            </div>
                            <div class="col">
                                <Modal isOpen={open} backdrop="static" {toggle}>
                                    <ModalHeader>Agregar Ciudad</ModalHeader>
                                    <ModalBody>
                                      Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                                      tempor incididunt ut labore et dolore magna aliqua.
                                    </ModalBody>
                                    <ModalFooter>
                                        <button type="button" class="btn boton_login" on:click={toggle}>Agregar</button>
                                        <button type="button" class="btn btn-secondary" on:click={toggle}>Cancelar</button>
                                    </ModalFooter>
                                </Modal>
                                <button type="button" class="btn boton_login mt-2 offset-md-2" on:click={toggle}><Icon name="plus" /></button>
                            </div>
                        </div>
                    </div>  
            
                    <div>
                        <div class="row d-flex justify-content-between">
                            <div class="col-9">
                                <FormGroup floating label="Avión">
                                    <select class="form-select mb-3" aria-label="Default select example" bind:value={id_avion_asociado}>
                                        {#each aviones as avion}
                                        <option value="{avion.id}">[{avion.id}] - {avion.modelo}</option>                  
                                        {/each}  
                                    </select>                                
                                </FormGroup>                
                            </div>
                            <div class="col">
                                <Modal isOpen={open_a} backdrop="static" {toggle} {size}>
                                    <ModalHeader>Agregar Avión</ModalHeader>
                                    <ModalBody>
                                      Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                                      tempor incididunt ut labore et dolore magna aliqua.
                                    </ModalBody>
                                    <ModalFooter>
                                        <button type="button" class="btn boton_login" on:click={toggleSm}>Agregar</button>
                                        <button type="button" class="btn btn-secondary" on:click={toggleSm}>Cancelar</button>
                                    </ModalFooter>
                                  </Modal>
                                <button type="button" class="btn boton_login mt-2 offset-md-2" on:click={toggleSm}><Icon name="plus" /></button>
                            </div>
                        </div> 
                               
                    </div>
            
                    <div>
                        <div class="row d-flex justify-content-center">
                            <div class="col-7">
                                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={registrar_vuelo}>Registrar Vuelo</button>
                            </div>
                        </div>
                    </div>
                    
                </Form>
            </div>
        </div>
    </div>
    
    


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
    div {
    text-align: justify;
    text-justify: inter-word;
    } 

  </style>

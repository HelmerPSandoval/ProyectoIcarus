<script>
    import { Tooltip, Alert, Label, Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Modal, ModalBody, ModalHeader, ModalFooter  } from 'sveltestrap';
    import { Router, Link, Route } from "svelte-routing";
    import Home from './Home.svelte';
    import { navigate } from "svelte-routing";
    import {usuario, mensaje_exito, mensaje_error} from "../utils/store";
    import { onMount } from "svelte";

    //Formulario registro de vuelo
	let fecha_salida = ''
	let hora_salida = ''
	let fecha_llegada = ''
	let hora_llegada = ''
    let valor_vuelo = 50000
	let id_ciudad_origen = 0
	let id_ciudad_destino = 0
	let id_avion_asociado = 0

    //Rellenar dropdowns de ciudades y avión
    let ciudades = []
    let aviones = []

    //Formulario modal de ciudades
    let nombre = ''
    let pais = ''

    //Formulario modal aviones
    let modelo = ''
    let capacidad = 50

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

    function llenar_dropdown_ciudades () {
        fetch('http://127.0.0.1:8000/ciudades/')
        .then(response => response.json())
        .then(data => {
                for(let i=0; i<data.length;i++){
                    
                    ciudades[i] = data[i]
                }
        }).catch(error => {
            console.log(error);
            return [];
        });
    };

    function llenar_dropdown_aviones () {
        fetch('http://127.0.0.1:8000/aviones/')
        .then(response => response.json())
        .then(data => {
                for(let i=0; i<data.length;i++){
                    
                    aviones[i] = data[i]
                }
        }).catch(error => {
            console.log(error);
            return [];
        });
    };
    
	let result = null
    
    let error_ = false;
    console.log("usuario:",$usuario);
    console.log("mensaje_exito:",$mensaje_exito);

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
                    valor_vuelo,
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
                $mensaje_exito = "Vuelo registrado con éxito.";
                
            }else{
                error_ = true;

            }

        } catch (error) {
            $mensaje_error = "Ha ocurrido un error durante el registro.";
        }
	}

    async function registrar_ciudad () {
        try {
            const res = await fetch('http://127.0.0.1:8000/ciudades/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nombre,
                    pais,
                })
            })
            const datos = await res.json()
            result = JSON.stringify(datos);
            console.log(result)
            if(datos.Return == 69)
            { 
                $mensaje_exito = "Ciudad registrada con éxito.";
                nombre = ''
                pais = ''
                llenar_dropdown_ciudades()
            }else{
                error_ = true;
                
            }

        } catch (error) {
            $mensaje_error = "Ha ocurrido un error durante el registro.";
            nombre = ''
            pais = ''
        }
        toggle();
	}

    async function registrar_avion () {
        try {
            const res = await fetch('http://127.0.0.1:8000/aviones/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    modelo,
                    capacidad,
                })
            })
            const datos = await res.json()
            result = JSON.stringify(datos);
            console.log(result)
            if(datos.Return == 69)
            { 
                
                $mensaje_exito = "Avión registrado con éxito.";
                modelo = ''
                capacidad = 50
                llenar_dropdown_aviones()
            }else{
                error_ = true;
                

            }

        } catch (error) {
            $mensaje_error = "Ha ocurrido un error durante el registro.";
            modelo = ''
            capacidad = 50
        }
        toggleSm();
	}

    let home = () => {
        $mensaje_exito=null;
        $mensaje_error=null;
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
<div>
    <button type="button" id="boton_home" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
    <Tooltip target="boton_home" placement="right">Volver al inicio</Tooltip>
</div>
<h1>Registrar nuevo vuelo</h1>
<h4>Ingrese la información del vuelo</h4>
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
                                        <div>
                                            <FormGroup floating label="Nombre ciudad">
                                                <Input class="h3 mb-3 fw-normal" type="text" bind:value={nombre}/>
                                            </FormGroup>
                                        </div>
                                        <div>
                                            <FormGroup floating label="País">
                                                <Input class="h3 mb-3 fw-normal" type="text" bind:value={pais}/>
                                            </FormGroup>
                                        </div>
                                    </ModalBody>
                                    <ModalFooter>
                                        <button type="button" class="btn boton_login" on:click={registrar_ciudad}>Agregar</button>
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
                                        <div>
                                            <FormGroup floating label="Modelo">
                                                <Input class="h3 mb-3 fw-normal" type="text" bind:value={modelo}/>
                                            </FormGroup>
                                        </div>
                                        <div>
                                            <FormGroup floating label="Capacidad">
                                                <Input class="h3 mb-3 fw-normal" type="number" min=1 bind:value={capacidad}/>
                                            </FormGroup>
                                        </div>
                                    </ModalBody>
                                    <ModalFooter>
                                        <button type="button" class="btn boton_login" on:click={registrar_avion}>Agregar</button>
                                        <button type="button" class="btn btn-secondary" on:click={toggleSm}>Cancelar</button>
                                    </ModalFooter>
                                  </Modal>
                                <button type="button" class="btn boton_login mt-2 offset-md-2" on:click={toggleSm}><Icon name="plus" /></button>
                            </div>
                        </div> 

                        <div>
                            <FormGroup floating label="Precio vuelo">
                                <Input class="h3 mb-3 fw-normal" type="number" bind:value={valor_vuelo}/>
                            </FormGroup>
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

<script>
    import {Spinner, Tooltip, Alert, Styles, Icon, Input, Form, FormGroup, Modal, ModalBody, ModalHeader, ModalFooter  } from 'sveltestrap';
    import { navigate } from "svelte-routing";
    import {usuario, mensajeExito, mensajeError} from "../utils/store";
    import * as editarVueloServices from "../utils/editarVueloServices";

    let vuelosPromise = editarVueloServices.cargarDropDownVuelos();
    let ciudadesPromise = editarVueloServices.cargarDropDownCiudades();
    let avionesPromise = editarVueloServices.cargarDropDownAviones();   
    
    let idvueloSeleccionado = -1;
    let vueloSeleccionadoPromise;

    function seleccionarVuelo(id){
        vueloSeleccionadoPromise = editarVueloServices.fetchVueloSeleccionado(id).then((result) => {
            vueloAEditar = result;
        });

    }

    let ciudadARegistrar = {};

    function registrarCiudad(){
        editarVueloServices.registrarCiudad(ciudadARegistrar);
        ciudadARegistrar = {};
        ciudadesPromise = editarVueloServices.cargarDropDownCiudades();
        toggle();
    }
    
    let avionARegistrar = {};

    function registrarAvion(){
        editarVueloServices.registrarAvion(avionARegistrar);
        avionARegistrar = {};
        vuelosPromise = editarVueloServices.cargarDropDownVuelos();
        toggleSm();
    }

    let vueloAEditar = {};

    function editarVuelo(){
        editarVueloServices.editarVuelo(vueloAEditar);
        vueloAEditar = {};
    }

    let home = () => {
        $mensajeExito=null;
        $mensajeError=null;
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
    let openA = false;

    const toggleSm = () => {
        openA = !openA;
    };
</script>

<Styles />
<div>
    <button type="button" id="boton_home" class="h3 mt-3 fw-normal btn boton_icarus" on:click={home}><Icon name="house-door-fill" /></button>
    <Tooltip target="boton_home" placement="right">Volver al inicio</Tooltip>
</div>
<h1>Editar Vuelo</h1>
<h4>Ingrese la información del vuelo</h4>
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
            <FormGroup floating label="Vuelo">
            <select class="form-select mb-3" aria-label="Default select example" bind:value={idvueloSeleccionado} on:change={() => seleccionarVuelo(idvueloSeleccionado)}>
                {#await vuelosPromise then vuelos}
                    {#each vuelos as vuelo}
                    <option value="{vuelo.id}">{vuelo.id}</option>                  
                    {/each}
                {/await}  
              </select>
            </FormGroup>
        </div>

        {#await vueloSeleccionadoPromise then vueloSeleccionado}
        <div>
            <FormGroup floating label="Fecha Salida">
                <Input class="h3 mb-3 fw-normal" type="date" bind:value={vueloAEditar.fecha_salida}/>
            </FormGroup>
        </div>
        
        <div>
            <FormGroup floating label="Hora Salida">
                <Input class="h3 mb-3 fw-normal" type="time" bind:value={vueloAEditar.hora_salida}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Fecha Llegada">
                <Input class="h3 mb-3 fw-normal" type="date" bind:value={vueloAEditar.fecha_llegada}/>
            </FormGroup>
        </div>

        <div>
            <FormGroup floating label="Hora Llegada">
                <Input class="h3 mb-3 fw-normal" type="time" bind:value={vueloAEditar.hora_llegada}/>
            </FormGroup>
        </div>
        {/await}  
        <div class="form-floating">
            <div class="row d-flex justify-content-between">
                <div class="col-9">
                    <div>
                        <FormGroup floating label="Ciudad Origen">
                        <select class="form-select mb-3" aria-label="Default select example" bind:value={vueloAEditar.id_ciudad_origen}>
                            {#await ciudadesPromise}
                                <Spinner color="primary" />
                            {:then ciudades}
                                {#each ciudades as ciudad}
                                <option value="{ciudad.id}">[{ciudad.id}] - {ciudad.nombre}</option>                  
                                {/each}
                            {/await}  
                        </select>
                        </FormGroup>
                    </div>
                </div>
                <div class="col">
                    <Modal isOpen={open} backdrop="static" {toggle}>
                        <ModalHeader>Agregar Ciudad</ModalHeader>
                        <ModalBody>
                            <div>
                                <FormGroup floating label="Nombre ciudad">
                                    <Input class="h3 mb-3 fw-normal" type="text" bind:value={ciudadARegistrar.nombre}/>
                                </FormGroup>
                            </div>
                            <div>
                                <FormGroup floating label="País">
                                    <Input class="h3 mb-3 fw-normal" type="text" bind:value={ciudadARegistrar.pais}/>
                                </FormGroup>
                            </div>
                        </ModalBody>
                        <ModalFooter>
                            <button type="button" class="btn boton_login" on:click={registrarCiudad}>Agregar</button>
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
                        <select class="form-select mb-3" aria-label="Default select example" bind:value={vueloAEditar.id_ciudad_destino}>
                            {#await ciudadesPromise}
                                <Spinner color="primary" />
                            {:then ciudades}
                                {#each ciudades as ciudad}
                                <option value="{ciudad.id}">[{ciudad.id}] - {ciudad.nombre}</option>                  
                                {/each}
                            {/await}  
                        </select>
                    </FormGroup>
                </div>
                <div class="col">
                    <button type="button" class="btn boton_login mt-2 offset-md-2" on:click={toggle}><Icon name="plus" /></button>
                </div>
            </div>
        </div>  

        <div>
            <div class="row d-flex justify-content-between">
                <div class="col-9">
                    <FormGroup floating label="Avión">
                        <select class="form-select mb-3" aria-label="Default select example" bind:value={vueloAEditar.id_avion_asociado}>
                            {#await avionesPromise}
                            <Spinner color="primary" />
                            {:then aviones}
                                {#each aviones as avion}
                                <option value="{avion.id}">[{avion.id}] - {avion.modelo}</option>                  
                                {/each}  
                            {/await}
                        </select>                                
                    </FormGroup>                
                </div>

                <div class="col">
                    <Modal isOpen={openA} backdrop="static" {toggle} {size}>
                        <ModalHeader>Agregar Avión</ModalHeader>
                        <ModalBody>
                            <div>
                                <FormGroup floating label="Modelo">
                                    <Input class="h3 mb-3 fw-normal" type="text" bind:value={avionARegistrar.modelo}/>
                                </FormGroup>
                            </div>
                            <div>
                                <FormGroup floating label="Capacidad">
                                    <Input class="h3 mb-3 fw-normal" type="number" min=1 bind:value={avionARegistrar.capacidad}/>
                                </FormGroup>
                            </div>
                        </ModalBody>
                        <ModalFooter>
                            <button type="button" class="btn boton_login" on:click={registrarAvion}>Agregar</button>
                            <button type="button" class="btn btn-secondary" on:click={toggleSm}>Cancelar</button>
                        </ModalFooter>
                      </Modal>
                    <button type="button" class="btn boton_login mt-2 offset-md-2" on:click={toggleSm}><Icon name="plus" /></button>
                </div>
            </div> 

            <div>
                <FormGroup floating label="Precio vuelo">
                    <Input class="h3 mb-3 fw-normal" type="number" bind:value={vueloAEditar.valor_vuelo}/>
                </FormGroup>
            </div>
                   
        </div>

        <div>
            <div class="row">
                <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={editarVuelo}>Editar Vuelo</button>
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

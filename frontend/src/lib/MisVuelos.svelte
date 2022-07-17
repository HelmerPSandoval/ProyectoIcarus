<script>
    import {Spinner, Tooltip, Alert, Table, Styles, Icon} from 'sveltestrap';
    import {usuario, mensajeExito, mensajeError} from "../utils/store";
    import { navigate } from "svelte-routing";
    import {cargarTabla, cancelarReserva} from "../utils/misVuelosServices";

    let rutUsuario = $usuario.rut
    let reservasPromise = cargarTabla(rutUsuario);

    function refrescarTabla(idReservaCancelada, rutUsuario){
        reservasPromise = cancelarReserva(idReservaCancelada, rutUsuario);
    }

    let goToHome = () => {
    mensajeExito.set(null);
    mensajeError.set(null);
    navigate("/home", {replace:true}); 
}

</script>
<Styles />
<div>
    <button type="button" id="boton_home" class="h3 mt-3 fw-normal btn boton_icarus" on:click={goToHome}><Icon name="house-door-fill" /></button>
    <Tooltip target="boton_home" placement="right">Volver al inicio</Tooltip>
</div>
<h1>Mis vuelos</h1>
<div class="row mx-auto mt-3" style="display: flex; width: 400px;">     
    {#if $mensajeExito != null} 
            <Alert style="text-align: center;" color="info" dismissible>{$mensajeExito}</Alert>
    {/if}           
    {#if $mensajeError != null} 
            <Alert style="text-align: center;" color="danger" dismissible>{$mensajeError}</Alert>
    {/if}      
</div>

<main>
    <div class="form-signin">
        {#await reservasPromise}
            <Spinner color="primary" />
        {:then reservas}        
            <Table hover bordered>
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Fecha Reserva</th>
                    <th>Valor vuelo</th>
                    <th>Cancelar</th>
                </tr>
                </thead>
                <tbody>
                    {#each reservas as reserva}
                        <tr>
                            <th scope="row">IC {reserva.id}</th>
                            <td>{reserva.fecha_reserva}</td>
                            <td>{reserva.valor_reserva}</td>
                            <td><button type="button" class="btn btn-danger"  on:click={() => refrescarTabla(reserva.id, rutUsuario)}><Icon name="x-circle" /></button></td>
                        </tr>
                    {/each}   
                    
                </tbody>
            </Table>
        {/await}           
    </div>
</main>

<style>

    .form-signin {
    width: 100%;
    max-width: 1060px;
    padding: 15px;
    margin: auto;
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

    
    h1 {
        color: #0b5394;
        font-weight: bold;
    }
   
    
</style>

import { writable } from "svelte/store";

export let usuario = writable(null);

export let mensaje_exito = writable(null);

export let mensaje_error = writable(null);



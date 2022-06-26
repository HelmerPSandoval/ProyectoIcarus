<script>
    import { Col, Container, Row, Styles, Icon, Input, Button, Form, FormGroup, Image, Card  } from 'sveltestrap';

	let username = 'lelouch@developer.op'
	let password = 'aweonao123'
	let result = null
	
	async function doPost () {
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
		result = JSON.stringify(datos)
	}
</script>

<Image alt="Icarus Airline" src="images/IcarusAirline.png" />
<main class="form-signin"> 

    <Form>
        <div class="form-floating">
            <FormGroup floating label="Email">
              <Input class="h3 mb-3 fw-normal" bind:value={username} />
            </FormGroup>
        </div>
        
        <div>
            <FormGroup floating label="Contraseña">
              <Input class="h3 mb-3 fw-normal" bind:value={password}/>
            </FormGroup>
        </div>
        
        <div>
            <button type="button" class="h3 mt-3 fw-normal btn boton_login" on:click={doPost}>Iniciar sesión</button>
        </div>
        
    </Form>
    
</main>
<p>
    Respuesta:
</p>
<pre>
{result}
</pre>






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

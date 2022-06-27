<script>
  import { Styles, Icon } from 'sveltestrap';
  import Login from './lib/Login.svelte';
  import Home from './lib/Home.svelte'
  import { Router, Link, Route } from "svelte-routing";
import Register from './lib/Register.svelte';
import ResetPassword from './lib/Reset_password.svelte';
</script>

<main>
	<Router>

    <Route path="/">
      <Login></Login>
    </Route>

		<Route path="/home">
			<Home></Home>
		</Route>
    
		<Route path="/register">
			<Register></Register>
		</Route>
    
		<Route path="/reset_password">
			<ResetPassword></ResetPassword>
		</Route>

	</Router>
</main>

<style>
  :root {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }

  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
  }

</style>

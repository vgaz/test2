function checkConnexion()
	{
	rep = requestServer('expert_mode=get_status')
	if (rep == "True")
		document.getElementById('connexion').innerHTML = "<a href='#' onclick='requestServer(" + '"expert_mode=quit"' + ");window.location.reload()'>Quit expert mode</a>"
	if (rep == "False")
		document.getElementById('connexion').innerHTML = "<a href='" + window.location.protocol + '//' + window.location.host + "/expert_mode_login/'>Connexion in expert mode</a>"
	}
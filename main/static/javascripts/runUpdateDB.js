
function runUpdateDB()
{
	document.getElementById("infoUpdateDB").innerHTML = '<img src="' + imageMainURL + '/loading.gif" title="updating database" style="width: 238px; height: 173px;" />'
	document.getElementById("button_update").disabled=true
	
	answ = requestServer("updateDB=true")
	
	document.getElementById("button_update").disabled=false
	document.getElementById("infoUpdateDB").innerHTML = answ
	
 }

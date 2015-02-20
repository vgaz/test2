// get results of tests 
// to post : param
// return response text or 

function requestServer(param)
{

	url = window.location.protocol + '//' + window.location.host + window.location.pathname + '../request/?' + param

	hReq = new XMLHttpRequest();
	hReq.open("GET", url , false)
	hReq.setRequestHeader("Content-type","application/x-www-form-urlencoded")
	hReq.onreadystatechange=function()
  		{
  		// la fonction de prise en charge du retour
		if ((hReq.readyState==4) && (hReq.status==200))		
			{
			return hReq.responseText
			}
		else
			{
			msg = "bad server return, req status = " + hReq.status
			alert(msg)
			return msg
			}
  		}

	hReq.send()
	return hReq.responseText

 }

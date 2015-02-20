
function launchCompare()
	{
	
	l_Ids = []
			
	// get all suites selected
	l_rep = document.getElementsByClassName("suite_header")
	
	for (ii=0; ii< l_rep.length; ii++) 
		{
		
		if (l_rep[ii].getElementsByClassName("DoCompareButton")[0].checked == true)
			{				
			l_Ids.push(parseInt(l_rep[ii].getAttribute("job_id"))) 	
			}
		}
	//alert(l_Ids)
	location.href='../compare/?jobs=' + l_Ids.toString()
//	ret = requestServer("compare=on&jobs=" + l_Ids.toString())
//	alert (ret)
	}



	
function displayCompareOption()
	{
	l_rep = document.getElementsByClassName("sequence_header")
	l_rep2 = document.getElementsByClassName("DoCompareButton");
			
	if (document.getElementById("doCompare").checked == true)
		{	
		for (ii=0; ii< l_rep.length; ii++) 
			l_rep[ii].style.display = "none"
			
		// add button to launch comparison
		for (ii=0; ii < l_rep2.length; ii++) 
			l_rep2[ii].style.display = "inline"
		
		
		}
	else
		{
		for (ii=0; ii< l_rep.length; ii++) 
			l_rep[ii].style.display = "block"
			
		// hide button to launch comparison
		for (ii=0; ii < l_rep2.length; ii++) 
			l_rep2[ii].style.display = "none"
		
			
		}
	}

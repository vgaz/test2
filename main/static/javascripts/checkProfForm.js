
function checkProfForm()
{
	bDisableSubmit = false

	// check if almost one rack is selected
	l_rep = document.getElementsByClassName("InputList")
	
	for (ii=0; ii< l_rep.length; ii++) 
		{
		l_inputs = l_rep[ii].getElementsByTagName("input");
		bOneCheckedAtLeast = false;
		for (i=0; i< l_inputs.length; i++) 
			{
			if (l_inputs[i].checked == 1)
				{
				bOneCheckedAtLeast = true;
				break;
				}
			}
		if (bOneCheckedAtLeast == false)
			{
			l_rep[ii].style.borderColor = "red";
			bDisableSubmit = true
			}
		else
			l_rep[ii].style.borderColor = "black";
		}


	
	
	if (bDisableSubmit)
		document.forms.mainForm.submit.disabled = true
	else
		document.forms.mainForm.submit.disabled = false

					
}

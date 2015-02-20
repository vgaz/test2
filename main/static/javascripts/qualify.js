function qualify(s_vmVersion)
	{
	answ = requestServer("qualify=" + s_vmVersion)
    if (answ == 'True')
    	alert('"' + s_vmVersion + '" will be evaluated in a few minute')
    else
    	alert('A problem occurred, please retry later')
	}
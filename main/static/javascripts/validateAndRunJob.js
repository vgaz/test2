function validateAndRunJob(s_vmVersion, s_debug)
	{
	oSelectOne = manualRunForm.elements["elt_suiteList"]
	index = oSelectOne.selectedIndex
	suite = oSelectOne.options[index].text                
	oSelectOne = manualRunForm.elements["elt_whenList"]
	index = oSelectOne.selectedIndex
	when = oSelectOne.options[index].text
                    
	if( confirm('Do you confirm the planification of the test suite\n' + suite + '\n' + when + '\non the ' + s_vmVersion))
		{
        url ='./index.py?planified=add&vmVersion=' + s_vmVersion + '&suiteName=' + suite + '&when=' + when + s_debug
        window.open(url, '_self')
        }
    }

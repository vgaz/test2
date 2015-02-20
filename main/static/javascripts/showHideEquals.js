function showHideEquals(buttonName, rawName)
	{
    button = document.getElementsByName(buttonName)
        
    l_elt = document.getElementsByName(rawName)  // find all elements
    if (button[0].value=='Show all')
    	{
    	newstyle = ""
        button[0].value="Hide equals"
    	for (ii=0; ii<l_elt.length; ii++)
        	l_elt[ii].style.display = newstyle
    	}
    else
        // hide equal scores
    	{
    	button[0].value = "Show all"
    	for (ii=0; ii<l_elt.length; ii++) 
        	{
            l_td = l_elt[ii].getElementsByClassName('score')   
            bEquals = true
            for (iii=0; iii<l_td.length; iii++)
        		{
            	if ( (l_td[0].getAttribute('nb_tests_ok') != l_td[iii].getAttribute('nb_tests_ok')) || (l_td[0].getAttribute('nb_tests_ko') != l_td[iii].getAttribute('nb_tests_ko')))
            		{
            		bEquals = false
            		break
            		}	
        		}
        	if (bEquals == true)
        		l_elt[ii].style.display = "none"
        	}    	
    	}
	}


function detailComp(seqId)
	{
  	document.getElementById('detail_' + seqId).innerHTML = ""
	
	button = document.getElementsByName("button_detail_"+ seqId)
	if (button[0].value=='X')
    	{
		// remove detail
        button[0].value="..."
        return
    	}
	else
        button[0].value="X"

	txtButton = "button_showHideEqualsDetail_" + seqId 
	txtDetail = '<input type="button" name="' + txtButton + '" value="Hide equals" onclick="showHideEquals(\'' + txtButton + '\', \'raw_test\')" />'
	txtDetail += '<table border="1" style="background-color:#E5E9BB;"><tr><th>test</th>'//<th>Status</th>'	
   
    // header
  	l_alltests = []
   	l_testTitle = []   // sans les doublons de nom
	
    hRaw = document.getElementById(seqId)
    // get all vm
    l_dataCol = hRaw.getElementsByClassName('score')
    	
    for (ii=0; ii<l_dataCol.length; ii++)
    	{
  		l_alltests[ii] = []
    	txtDetail += "<th>VM " + ii + "</th>"
    	// find tests for this column
    	l_t = l_dataCol[ii].getElementsByClassName('test')   
  	   	for (iii=0; iii<l_t.length; iii++)
  	   		{
  	   		t_name = l_t[iii].getAttribute('name')
  	   		// append test fort each column
  	   		l_alltests[ii].push( [t_name, l_t[iii].getAttribute('nbtestsok'), l_t[iii].getAttribute('nbtestsko'), l_t[iii].getAttribute('status'), l_t[iii].getAttribute('comment')])
  	   		
  	   		if (l_testTitle.indexOf(t_name) == -1)
  	   			l_testTitle.push(t_name)
  	   		}
    	}
    txtDetail += "</tr>"
   
   	// content for each test
   	for (iii=0; iii<l_testTitle.length; iii++)
   		{
   		txtDetail += '<tr name="raw_test"><td style="text-align:left;">' + l_testTitle[iii] 

   		// content for each data column
	   	for (ii=0; ii<l_dataCol.length; ii++)
	    	{
	   		ratio = "NA"
   		    txtDetail += '<td valign="top" style="text-align:center;">'
	   		for (ttt=0; ttt<l_alltests[ii].length; ttt++)
	   			{
	   			if (l_testTitle[iii] == l_alltests[ii][ttt][0]) // meme nom, on met le ratio
	   				{
	   		        ratio = l_alltests[ii][ttt][1] + '/' +  l_alltests[ii][ttt][2]
	   		        if (l_alltests[ii][ttt][3] == "Success")
	   		        	bgCol = '#00FF00'
	   		        else
	   		        	bgCol = '#FF0000'
	   		        		
	           		txtDetail += '<div class="score" ratio="' + ratio + '"  style="width: 150px;"/>' 
	           		txtDetail += '<div style="background-color:' + bgCol + ';">' + l_alltests[ii][ttt][3] +'</div><br/>'/* status */ 
	           		txtDetail += l_alltests[ii][ttt][1] + ' ok / ' +  l_alltests[ii][ttt][2] + ' ko // ' +  (parseInt(l_alltests[ii][ttt][1]) + parseInt(l_alltests[ii][ttt][2]))
	   		        if (l_alltests[ii][ttt][4] != 'None')
	   		        	txtDetail += '<br/>' + l_alltests[ii][ttt][4]  /* comment */
	           		txtDetail += '</div>' 
	   				}
	   			}
		    if (ratio  == "NA")
	   			// si on passe ici, c'est qu'on a pas trouvé de test pour cette colonne, bouchon
		    	txtDetail += '<div class="score" ratio="NA">?</div>'
  
		    txtDetail += "</td>"
	    	}
   	    txtDetail += '</tr>'
   		}
    txtDetail += '</table>'
    //myWindow.document.write(txtDetail)
  	document.getElementById('detail_' + seqId).innerHTML = txtDetail

	}
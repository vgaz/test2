//
// All functions used for payy ci web pages
//
	
function changeComp()
    {
    e = document.getElementById("component_choice")
    e.style.backgroundColor="yellow"
    rep = requestServer('setComponent=' + e.options[e.selectedIndex].text)
    e.style.backgroundColor="white"
    }

function checkConnexion()
	{
	rep = requestServer('expert_mode=get_status')
	if (rep == "True")
		{
			txt = "Your're now connected in expert mode. It gives you more rights to manage CI results."
			document.getElementById('connexion').innerHTML = "<a href='#' onclick='requestServer(" + '"expert_mode=quit"' + ");window.location.reload()'>Quit expert mode</a>"
			document.getElementById('login').innerHTML = "<p>" + txt + "</p><br /><p><a href='../home'>Home</a></p>"
		}
	if (rep == "False")
		document.getElementById('connexion').innerHTML = "<a href='../expert_mode_login/'>Connexion in expert mode</a>"
	}


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
			l_rep[ii].style.borderColor = "white";
		}

	if (bDisableSubmit)
		document.forms.mainForm.submit.disabled = true
	else
		document.forms.mainForm.submit.disabled = false
					
}

function colorScores()
	{
	// change background color for all elements with class score depending on attribute "ratio"
	l_rep = document.getElementsByClassName("score");

	for (i=0; i < l_rep.length; i++) 
		l_rep[i].style.backgroundColor = getScoreColor( parseInt(l_rep[i].getAttribute("ratio")))
	

}

function displayCompareOption()
	{
	l_rep = document.getElementsByClassName("sequence_header")
	l_rep2 = document.getElementsByClassName("DoCompareButton")
			
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


function getScoreColor(percentScore)
{
    // return a tupple of rgb color from a given perecnt score
	// percentScoreis INT
	
    if (percentScore < 0 || percentScore > 100)
        return [255, 255, 255]
    
    if (percentScore < 75)
    {
    	//# dégradé de rouge pur à orange clair (= 255,231,0)
        i_r = 255 
        i_g = (percentScore * 231) / 75
        i_b = 0
	}
    else
    {
    	//# dégradé de orange clair (= 255,231,0) à vert pur
        i_r = 255 - 255 * (percentScore - 75) / 25 
        i_g = 231 + (255 - 231) * (percentScore - 75) / 25
        i_b = 0
    }
    
    i_r = Math.floor( i_r)
    i_g = Math.floor( i_g)
    i_b = Math.floor( i_b)
    return ("rgb(" + i_r + "," + i_g + "," + i_b + ")")
		
}
	
// get results of tests 
// to post : list of test ids 
// to get in response : a json structure of all test results

function getTestsRslts(seq_id)
{
	// request for test results from sequence primary key
	return requestServer("seqTestsRslts=" + seq_id)
}

function displaySequenceResults(seq_pk)
{
	// request for test results
	if (document.getElementById(seq_pk).innerHTML == "")
		{
		// ask for seq results
		ret = getTestsRslts(seq_pk)

		hData = JSON.parse(ret)
  		s_div = '<table border="1" width="100%">'
  		s_div += '<tr><th>Functionality</th/><th>Test name</th/><th>status</th><th>success</th><th>failed</th><th>comment</th><th>log file</th></tr>'
		for (index = 0; index < hData.tests.length; index++)
			{
			s_div += "<tr><td>" + hData.tests[index].functionality + "</td>"
			s_div += "<td class='td1'>" + hData.tests[index].name + "</td>"
			if (hData.tests[index].status == 1) // 1 means status ok
				{
				className = "tdSuccess"
				s_status = "Succcess"
				}
			else			
				{
				className = "tdFailure"
				s_status = "Failure"
				}
				
			s_div += "<td class='" + className + "'>" + s_status + "</td>"
			s_div += "<td class='td2'>" + hData.tests[index].success + "</td>"
			s_div += "<td class='td2'>" + hData.tests[index].failed + "</td>"			
			s_div += "<td class='td2'>" + hData.tests[index].comment + "</td>"			
			s_div += "<td>" + hData.tests[index].log_file + "</td></tr>"
			}
		s_div += "</table>"
		document.getElementById(seq_pk).innerHTML = s_div
		}
	else
		document.getElementById(seq_pk).innerHTML = ""
 }

function displayCompareTestsResults(divId, s_testsList)
{
	idContent = "detail_comp_" + divId
	hDiv = document.getElementById(idContent)
	if (hDiv.innerHTML == "")
		{
		reps = []
		tnames = []
		// get all test for each seq/vm
		seqId = document.getElementById('seq_' + divId)
		
		l_bins = seqId.getElementsByClassName("score")
		
		for (index=0; index < l_bins.length; index++)
			{
			seq_id = l_bins[index].getAttribute("seq_id")
			//alert("test list " + l_ids)
			rep = getTestsRslts(seq_id)
			jp = JSON.parse(rep)
			// add bin version
			jp.bin_version = l_bins[index].getAttribute("bin_version")
			reps.push(jp)
			
			// complete disctinct test names table
			for (var i in jp.tests)
				if (tnames.indexOf(jp.tests[i].name) == -1)
					tnames.push(jp.tests[i].name)
        
			}
			
		s_div = '<table class="table2">'
		s_div += '<tr><th class="td1">test name</th>'
		// bin colls
		for (index=0; index < l_bins.length; index++)
			s_div += '<th class="td1">' + l_bins[index].getAttribute("bin_version") + '</th>'
		
		for (index in tnames)
			{
			s_div += "<tr><td class='td1' id='" + divId + tnames[index] + "'>" + tnames[index] + "</td>"
			
			// add score for each bin version
			t_resbin = ""
     		bTfound = 0
			for (ii in reps) 
				{
				//t_resbin += reps[ii].bin_version
				for (itest in reps[ii].tests)  // find the right test to display
					{
					if (reps[ii].tests[itest].name == tnames[index])
						{
						// color status
						if (reps[ii].tests[itest].status == 1) // means success
							{
							className = "tdSuccess"
							s_status = "Success"
							}
						else
							{
							className = "tdFailure"
							s_status = "Failure"
							}

						t_resbin += "<td class='" + className + "'>" + s_status + "<br/>"
						t_resbin += reps[ii].tests[itest].comment + "<br/>"
						t_resbin += "</td>"
						bTfound = 1
						break
						}
					}
				if (bTfound == 0)
					t_resbin += "<td class='overview_2'></td>" // complete td with unknown status for a test that is not available for this bin version				
				}
			s_div += t_resbin + "<tr/>"
			
			}	
		s_div += "</table>"

		document.getElementById(idContent).innerHTML = s_div
		
		
//		// variante pour afficher dans la colonne des vm du tableau principal
//		for (ii in reps) 
//			{			
//		    s_divPerCol = ""
//			for (index in tnames)
//				{
//			    // resize td heigth from test name td
//				cellHeight = document.getElementById(divId + tnames[index]).clientHeight
//				s_divPerCol += "<tr style='height:" + cellHeight + "px'>" 
//				for (itest in reps[ii].tests)  // find the right test to display
//					{
//					if (reps[ii].tests[itest].name == tnames[index])
//						{
//						// color status
//						if (reps[ii].tests[itest].status == "Failure")
//							className = "tdFailure"
//						else
//							className = "overview_2"
//						
//						s_divPerCol += "<td class='" + className + "'>" + reps[ii].tests[itest].status + "<br/>"
//						s_divPerCol += reps[ii].tests[itest].comment + "<br/>"
//						s_divPerCol += "</td>"
//						bTfound = 1
//						break
//						}
//					}
//				if (bTfound == 0)
//					t_resbin += "<td class='overview_2'></td>" // complete td with unknown status for a test that is not available for this bin version			
//				s_divPerCol += "<tr>" 
//				}
//		    document.getElementById("test_detail_" + reps[ii].bin_version).innerHTML = "<table class='table2'>" + s_divPerCol + "</table>"
//			
//	    
//			} 
			// fin variante
				

		}
	else
		document.getElementById(idContent).innerHTML = ""
 }

function launchCompare()
	{
	l_Ids = []	
	// get all suites selected
	l_rep = document.getElementsByClassName("suite_header")
	
	for (ii=0; ii< l_rep.length; ii++) 
		{
		
		if (l_rep[ii].getElementsByClassName("DoCompareButton")[0].checked == true)
			{				
			l_Ids.push(parseInt(l_rep[ii].getAttribute("job"))) 	
			}
		}
	location.href='../compare/?jobs=' + l_Ids.toString()
	}
	
function qualify(s_vmVersion)
	{
	answ = requestServer("qualify=" + s_vmVersion)
    if (answ == 'True')
    	alert('"' + s_vmVersion + '" will be evaluated in a few minute')
    else
    	alert('A problem occurred, please retry later')
	}

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

function setSuiteScore()
	{
	l_rep = document.getElementsByClassName("suite_div")	
	for (ii=0; ii< l_rep.length; ii++) 
		{
		ratio = 0
		nbOk = 0
		nbTotalTests = 0
		
		l_seqsScore = l_rep[ii].getElementsByClassName("score")

		for (i=0; i< l_seqsScore.length; i++) 
			{
			nbOk += parseInt(l_seqsScore[i].getAttribute("nb_tests_ok"))
			nbTotalTests += parseInt(l_seqsScore[i].getAttribute("nb_tests"))
			}
		ratio = parseInt((100*nbOk)/nbTotalTests)
		if (nbTotalTests == 0)
			l_rep[ii].getElementsByClassName("suite_score")[0].innerHTML = "unavailable"
		else
			l_rep[ii].getElementsByClassName("suite_score")[0].innerHTML = ratio +  "% (" + nbOk +"/" + nbTotalTests + ")"
		l_rep[ii].getElementsByClassName("suite_header")[0].style.borderColor = getScoreColor(ratio)
		}
	}

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

function uploadComment(bin_version)
    {
    comment = document.getElementById('txtarea_general_comment').value.replace("\n", "\\n")
    request = 'set_bin_version_comment={"bin_version":"' + bin_version + '","comment":"' + comment + '"}'
    document.getElementById('txtarea_general_comment').innerHTML = requestServer(request)
    }   

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

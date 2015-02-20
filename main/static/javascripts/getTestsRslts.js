// get results of tests 
// to post : list of test ids 
// to get in response : a json structure of all test results

function getTestsRslts(s_testsList)
{
	// request for test results
	return requestServer("testsList=" + s_testsList)

 }

function displaySequenceResults(divId, s_testsList)
{
	// request for test results
	if (document.getElementById(divId).innerHTML == "")
		{
		
		ret = getTestsRslts(s_testsList)

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
				
			s_div += "<td  class='" + className + "'>" + s_status + "</td>"
			s_div += "<td  class='overview_2'>" + hData.tests[index].success + "</td>"
			s_div += "<td  class='overview_2'>" + hData.tests[index].failed + "</td>"			
			s_div += "<td>" + hData.tests[index].comment + "</td>"			
			s_div += "<td>" + hData.tests[index].log_file + "</td></tr>"
			}
		s_div += "</table>"
		document.getElementById(divId).innerHTML = s_div
		}
	else
		document.getElementById(divId).innerHTML = ""
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
			l_ids = l_bins[index].getAttribute("tests_ids")
			//alert("test list " + l_ids)
			rep = getTestsRslts(l_ids)
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
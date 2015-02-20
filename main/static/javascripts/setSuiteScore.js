

	
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

		l_rep[ii].getElementsByClassName("suite_score")[0].innerHTML = ratio +  "% (" + nbOk +"/" + nbTotalTests + ")"
		l_rep[ii].getElementsByClassName("suite_header")[0].style.borderColor = getScoreColor(ratio)
		
		}
}

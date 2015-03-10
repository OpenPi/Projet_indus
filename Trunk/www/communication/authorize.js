var urlAuthorization = '../authorize/';

var user = "";
var password = "";

function postLogin()
{

	user = document.forms['login'].user.value;
	password = document.forms['login'].password.value;

	$.ajax //We send a GET Request for take the user's commands
	({
			
			url : urlAuthorization, // We send a request with the date from which we want the data

			type : "POST",

			data : 'user='+user+'&password='+password,

		 	success : function(resultat, statut)
		 	{
		 		console.log(statut);
		 		console.log(user);
		 		console.log(password);	
		 		$("#error").html("<p>Congrats, you are logged :)</p>");

		 		$(location).attr('href','ihm.html');
		 	},

		 	error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '401')
		 		{
		 			$("#error").html("<p>There is an error, the query found nothing</p>"); //We send on the screen the table
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

	});

}

	
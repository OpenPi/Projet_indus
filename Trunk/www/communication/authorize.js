var urlAuthorization = '../authorize/';

var user = "";
var password = "";

function displayLoginBox()
{
	if($("#login").css("display: inline-block;"))
	{
		$("#login").css("display: none;");
		$("#disconnect").css("display: inline-block;");
	}
	else
	{
		$("#disconnect").css("display: none;");
		$("#login").css("display: inline-block;");
	}
}



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
		 		//$(location).attr('href','ihm.html');
		 		displayLoginBox();

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

function postDisconnect()
{
	$.ajax //We send a GET Request for take the user's commands
	({
			
			url : urlAuthorization, // We send a request with the date from which we want the data

			type : "DELETE",

			//data : 'user='+user+'&password='+password,

		 	success : function(resultat, statut)
		 	{
		 		displayLoginBox();

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

	
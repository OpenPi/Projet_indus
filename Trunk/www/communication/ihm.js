/*
 * Variables Declaration
 */

/*
 * Address variables Declaration
 */
var urlAllMeasure = '../measures/';
var urlLimitMeasure = '?xlast=';
var urlDateMeasure = '?time=';
var urlReadUserCommand = '../usercommands/';
var urlCreateUserCommand = '../usercommands/';
var urlHardwareConfiguration = '../hardwareconfigurations/';
var urlAuthorization = '../authorize/';
var urlAlert = '../alerts/';

/*
 * Login variables Declaration
 */
var user = "";
var password = "";


/*
 * General variables Declaration
 */
var order = 10;
var i = 0;
var sensorType = "";
var urlAll = "";
var urlLimit = "";
var urlDAte = "";

var log = '<form id="login">'
	log += '<input type="text" name="user" placeholder="user" id="user"  required/>'
	log += '<input type="password" name="password" placeholder="password" id="password" required/>'
	log += '<input type="button" value="Valid" id="valid" onclick="postLogin();"/>'
	log += '</form>';

var delog = '<form id="disconnect"><input type="button" value="disconnect" id="disconnect" onclick="postDisconnect();"/></form>';


/*
 * Address variables Declaration
 */

 //Execute the get function each seconds
setInterval(getMeasure, 5000); 

//Execute the get function each seconds
setInterval(getMeasuresForChart, 5000); 

//Execute the get function each seconds
setInterval(getUserCommand, 5000); 

//Execute the get function each seconds
setInterval(getAlert, 5000); 

/**
 * Function to select the data's sensor to display
 * @method typeSensor
 * @return {} sensorType
 */
function typeSensor()
{

	//For each sensor type
	for(i = 0; i < document.getElementById("sensorTypeRequest").elements.length; i++)
	{
		//if the radio button is checked
		if(document.getElementById("sensorTypeRequest").elements[i].checked)
		{
			//we return the sensor type wich is checked
			return sensorType = document.getElementById("sensorTypeRequest").elements[i].value;
			break;
		}
	}

}

/**
 * Function to take the measures in the database and draw a table whith it
 * @method getMeasure
 * @return 
 */
function getMeasure()
{
	//Recover the limit value
	var xlast = $("#xlast").val();

	//Recover the date limit
	var calendar = $("#timestamp").val();
	calendar = "%22" + calendar + ":00%22";

	//Recover the sensor type
	sensorType = typeSensor();

	//If we don't have any specific sensor type 
	if(!$.isNumeric(sensorType))
	{
		//We take all datas (with the limit)
		urlAll =  urlAllMeasure + urlLimitMeasure + xlast;
		urlLimit =  urlAllMeasure + urlLimitMeasure + xlast;
		urlDAte =  urlAllMeasure + urlLimitMeasure + xlast;
	}
	else
	{
		//Else, we take only the data for the specific sensor type
		urlAll = urlAllMeasure + sensorType + urlLimitMeasure + xlast;
		urlLimit = urlAllMeasure + sensorType + urlLimitMeasure + xlast;
		urlDAte = urlAllMeasure+ sensorType + urlDateMeasure + calendar;
	}
    //if we don't have limits, we send a GET Request to take the sensors' data
	if($.isEmptyObject(xlast) && (calendar == "%22:00%22" || calendar == "%22undefined:00%22")) 
	{
		$.ajax
		({
			//Target file in the server
		 	url : urlAllMeasure + sensorType, 

		 	type : "GET",

		 	//We receive the data in JSON format
		 	dataType : 'json', 

		 	success : displayMeasure,

		 	//If error
	 		error : function(resultat, statut, erreur)
		 	{
		 		//if we have a 404 error
		 		if(resultat['status'] == '404')
		 		{
		 			//We send on the error message
		 			$("#measure").html("<p>There is an error, the query found nothing</p>"); 
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

		});	
	}
	//If we have a limit for the number of data
	else if(!$.isEmptyObject(xlast) && (calendar == "%22:00%22" || calendar == "%22undefined:00%22")) 
	{
		$.ajax
		({
			url : urlLimit, 

			type : "GET",

		 	dataType : 'json',

		 	success : displayMeasure,

	 		error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>");
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

		});	
	}
	//If we have a limit of date
	else if($.isEmptyObject(xlast) && calendar != "%22:00%22") 
	{
		$.ajax	
		({
			
			url : urlDAte,

			type : "GET",

		 	dataType : 'json',

		 	success : displayMeasure,

	 		error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>");
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

		});			
	}

}





/**
 * Function to take the measures in the database and draw a chart whith it
 * @method getMeasuresForChart
 * @return 
 */
function getMeasuresForChart()
{
	var xlastChart = $("#xlastChart").val();

	sensorType = typeSensor();

	//If we have a sensor type, we can draw the chart
	if(sensorType != "")
	{
		//If we have a limit, we draw the chart with a limit number of data
		if(!$.isEmptyObject(xlastChart))
		{
			$.ajax
			({
					
					url : urlAllMeasure + sensorType + urlLimitMeasure + xlastChart,

					type : "GET",

				 	dataType : 'json',

				 	success : drawChart,

	 				error : function(resultat, statut, erreur)
				 	{
				 		if(resultat['status'] == '404')
				 		{
				 			$('#curve_chart').html("<p> The chart is impossible to draw (no data) </p>");
				 			console.log(resultat['status'] + " : " + erreur);
				 		}
				 	}

			});

		}
		//Else, we draw the chart all data
		else
		{
			$.ajax //We send a GET request to draw the chart
			({
					
					url : urlAllMeasure + sensorType, // We send a request with the date from which we want the data

					type : "GET",

				 	dataType : 'json',

				 	success : drawChart,

	 				error : function(resultat, statut, erreur)
				 	{
				 		if(resultat['status'] == '404')
				 		{
				 			$('#curve_chart').html("<p> The chart is impossible to draw (no data) </p>");
				 			console.log(resultat['status'] + " : " + erreur);
				 		}
				 	}

			});			
		}
	}
	//If we don't have a specific sensor type
	else
	{
		$('#curve_chart').html("<p>Sorry, we don't have only one type of data, the draw is impossible</p>")
	}

}




/**
 * Function to take the user command in the database and draw a table whith it
 * @method getUserCommand
 * @return 
 */
function getUserCommand()
{

	$.ajax
	({
			
			url : urlReadUserCommand,

			type : "GET",

		 	dataType : 'json',

		 	success : displayUserCommand,

	 		error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>");
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

	});

}




/**
 * Function to take the alert in the database and draw a table whith it
 * @method getAlert
 * @return 
 */
function getAlert()
{

	$.ajax
	({
			
			url : urlAlert,

			type : "GET",

		 	dataType : 'json',

		 	success : displayAlert,

	 		error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>");
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

	});

}

/**
 * Function to take the hardware configuration in the database and draw a form whith it
 * @method getHardwareConfiguration
 * @return 
 */
function getHardwareConfiguration()
{

	$.ajax
	({
			
			url : urlHardwareConfiguration,

			type : "GET",

		 	dataType : 'json',

		 	success : displayHardwareConfiguration,

	 		error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>");
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

	});

}






/**
 * This function draw a form to select the sensor data to display 
 * @method displayHardwareConfiguration
 * @param {} text
 * @return 
 */
function displayHardwareConfiguration(text)
{
	//We take the number of records in the form
	var data_long = text['hardwareConfigurations'].length; 
	var name = '';
	var id = '';

	//We initialize the form to display
	var txt_measures = ''; 

	txt_measures += '<input type="radio" name="sensor" value="" id="nothing" checked/> <label>"Nothing"</label><br />';

	//We write in the string the data from the DB
	for(i=0; i<data_long; i++) 
	{

		id = text['hardwareConfigurations'][i]['id'];
		name = text['hardwareConfigurations'][i]['name'].split(" ");

		txt_measures += '<input type="radio" name="sensor" value="'+id+'" id="'+name[1]+'"/> <label>"'+name[1]+'"</label><br />';
	}

	//We send on the screen the form
	$("#sensorTypeRequest").html(txt_measures); 
}






/**
 * This function draw a table with the alerts 
 * @method displayAlert
 * @param {} text
 * @return 
 */
function displayAlert(text)
{
	var data_long = text['alerts'].length; 

	var name = '';
	var id = '';
	var cpt = 0;

	var txt_alert = '';

	txt_alert += '<table id="alert_display"><th>Hardware Name</th><th>Name</th><th>Description</th><th>TimeStamp</th><th>Delete</th>';

	for(i=0; i<data_long; i++)
	{
		if(text['alerts'][i]['is_viewed'] == '0')
		{

			id = text['alerts'][i]['id'];
			name = text['alerts'][i]['hardware_name'].split(" ");

			txt_alert += "<tr><td>" + name[1] + "</td>";
			txt_alert += "<td>" + text['alerts'][i]['alert_name'] + "</td>";
			txt_alert += "<td>" + text['alerts'][i]['alert_description'] + "</td>";
			txt_alert += "<td>" + text['alerts'][i]['timestamp'] + "</td>";
			txt_alert += "<td> <input type='button' value='I seen it' onclick='updateAlert("+text['alerts'][i]['alert_id']+");'> </td></tr>";

			cpt++;
		}
		else
		{
			continue;
		}
	}

	txt_alert += "</table>";

	if(cpt != 0)
	{
		//We send the form on the screen
		$("#alert").html(txt_alert); 
	}
	else if(data_long != 0)
	{
		//We send a message on the screen when all alerts is red
		$("#alert").html("<p>You red all alerts!</p>"); 
	}
	else
	{
		//We send a message on the screen if we don't have any alert
		$("#alert").html("<p>You don't have any alert!</p>"); 
	}
}







/**
 * This function draw a table for the measures 
 * @method displayMeasure
 * @param {} text
 * @return 
 */
function displayMeasure(text)
{

	var data_long = text['measures'].length;

	var txt_measures = '<table id="measure_display"><th>Hardware Name</th><th>Value</th><th>TimeStamp</th>';

	for(i=0; i<data_long; i++)
	{
		var sens = text['measures'][i]['hardware_name'].split(" ");

		var typeSensor = sens[1];

		txt_measures += "<tr><td>" + typeSensor + "</td>"
		txt_measures += "<td>" + text['measures'][i]['value'] + "</td>"
		txt_measures += "<td>" + text['measures'][i]['timestamp'] + "</td></tr>"
	}
	txt_measures += "</table>";

	$("#measure").html(txt_measures);

}

/**
 * This function draw a table with the user's commands
 * @method displayUserCommand
 * @param {} text
 * @return 
 */
function displayUserCommand(text)
{
		var data_long = text['commandes'].length;

		var txt_userCommand = '<table id="userCommand_display"><th>Command</th><th>Target Name</th><th>Value</th><th>TimeStamp</th><th>Done</th>';

		for(i=0; i<data_long; i++)
		{

			txt_userCommand += "<tr><td>" + text['commandes'][i]['command'] + "</td>"
			txt_userCommand += "<td>" + text['commandes'][i]['name'] + "</td>"
			txt_userCommand += "<td>" + text['commandes'][i]['value'] + "</td>"
			txt_userCommand += "<td>" + text['commandes'][i]['timestamp'] + "</td>"
			txt_userCommand += "<td>" + text['commandes'][i]['done'] + "</td></tr>"
		}
		txt_userCommand += "</table>";

		$("#userCommand").html(txt_userCommand);

}

/**
 * This function send a request to the server to records a new user's command in the DB
 * @method drawChart
 * @param {} text
 * @return 
 */
function drawChart(text) 
{

	var data_long = text['measures'].length;

	var sens = text['measures'][0]['hardware_name'].split(" ");

	var typeSensor = sens[1];

	//We initialize the increment variable
	var increment = data_long - 1;

	//We create a new DataTable to draw the chart
	var data = new google.visualization.DataTable(); 
	//We ceate the first column
	data.addColumn('number', 'Time'); 
	//We ceate the second column
	data.addColumn('number', 'Order'); 
	//We ceate the third column
	data.addColumn('number', typeSensor); 

	var val = 0;
	var j = 0;
	var time;

	if(!$.isEmptyObject(document.forms['orderRequest'].order.value))
	{
		//We take the regulation order in the HTML form
		order = document.forms['orderRequest'].order.value; 
	}
	else
	{
		order = 10;
	}

	for(increment; increment>0; increment--)
	{
		//We take the measure value in the request answer
		val = text['measures'][increment]['value']; 

		//We take the measure value in the request answer
		time = text['measures'][increment]['timestamp']; 

		//We create a new row in the DataTable
		data.addRows([[j,parseFloat(order),parseFloat(val)]]); 
		j++; 

	}

	//We create an option variable for the chart feature
    var options = 
    {
      title: 'PID ' + typeSensor,
      vAxis: {title: typeSensor},
      hAxis: {title: "Time"},
      curveType: 'function',
      legend: { position: 'bottom' }
    };


    //We create a new chart
    var chart = new google.visualization.LineChart(document.getElementById('curve_chart')); 

    //We draw the chart
    chart.draw(data, options); 
}






/**
 * Function to display the connect form
 * @method displayLoginBox
 * @return 
 */
function displayLoginBox()
{
	//Display login form
	$("#connect").html(log);

	//Hide disconnect form and alert table
	$("#connected").hide();
	$("#alert").hide();

	//Display connect form
	$("#disconnected").show();
}

/**
 * Function to display the disconnect form
 * @method deDisplayLoginBox
 * @return 
 */
function deDisplayLoginBox()
{
	//Display disconnect form
	$("#connect").html(delog);

	//Display connect form and alert table
	$("#connected").show();
	$("#alert").show();

	//Hide connect form
	$("#disconnected").hide();

	//Call getHardwareConfiguration function
	getHardwareConfiguration();
}


/**
 * Function to connect to the server
 * @method postLogin
 * @return 
 */
function postLogin()
{

	user = document.forms['login'].user.value;
	password = document.forms['login'].password.value;

	//We send a POST Request to connect the user
	$.ajax 
	({
			
			url : urlAuthorization,

			type : "POST",

			//Data which will be sent to the server
			data : 'user='+user+'&password='+password,

		 	success : deDisplayLoginBox,

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

/**
 * Function to disconnect from the server
 * @method postDisconnect
 * @return 
 */
function postDisconnect()
{
	//We send a DELETE Request to disconnect the user
	$.ajax 
	({
			
			url : urlAuthorization,

			type : "DELETE",

		 	success : displayLoginBox,

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


/**
 * Function to send a request to the server to records a new user's command in the DB
 * @method postUserCommand
 * @return 
 */
function postUserCommand()
{
	//We take the command type in the HTML form
	var type = $("#type").val(); 

	//We take the command type in the HTML form
	var command = $("#command").val(); 

	//We take the command name type in the HTML form
	var targetName = $("#targetName").val(); 

	//We take the command value type in the HTML form
	var val = $("#val").val(); 

	//We send a POST Request to save a new user command
	$.ajax 
	({
			
			url : urlCreateUserCommand,

			type : "POST",

			//Data which will be sent to the server
			data : 'type='+type+'&command='+command+'&targetName='+targetName+'&value='+val,

		 	success : getUserCommand,

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

/**
 * Function to modify the alert status (view or not)
 * @method updateAlert
 * @param {} id
 * @return 
 */
function updateAlert(id)
{
	//We send a PUT request to modify a record on the database
	$.ajax(
	{

	  url: urlAlert + id,

	  type: 'PUT',

	  //the parameter of the request
	  data: "show=1",

	  success: displayAlert

  	}
  );
}
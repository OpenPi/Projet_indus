var urlAllMeasure = '../measures/';
var urlLimitMeasure = '?xlast=';
var urlDateMeasure = '?time=';
var urlReadUserCommand = '../usercommands/';
var urlCreateUserCommand = '../usercommands/';
var urlHardwareConfiguration = '../hardwareconfigurations/';
var urlAuthorization = '../authorize/';

var order = 10;
var i = 0;
var sensorType = "";
var urlAll = "";
var urlLimit = "";
var urlDAte = "";

setInterval(getMeasure, 5000); //Execute the get function each seconds
setInterval(getMeasuresForChart, 5000); //Execute the get function each seconds
setInterval(getUserCommand, 5000); //Execute the get function each seconds

function typeSensor()
{

	for(o = 0; o < document.getElementById("sensorTypeRequest").elements.length; o++)
	{
		if(document.getElementById("sensorTypeRequest").elements[o].checked)
		{
			return sensorType = document.getElementById("sensorTypeRequest").elements[o].value;
			break;
		}
	}

}


function getMeasure()
{

	var xlast = $("#xlast").val();

	var calendar = $("#timestamp").val();
	calendar = "%22" + calendar + ":00%22";

	sensorType = typeSensor();

	if(!$.isNumeric(sensorType))
	{
		urlAll =  urlAllMeasure;
		urlLimit =  urlAllMeasure;
		urlDAte =  urlAllMeasure;
	}
	else
	{
		urlAll = urlAllMeasure + sensorType;
		urlLimit = urlAllMeasure + sensorType + urlLimitMeasure + xlast;
		urlDAte = urlAllMeasure+ sensorType + urlDateMeasure + calendar;
	}

	if($.isEmptyObject(xlast) && calendar == "%22:00%22") //if we don't have limits, we send a GET Request for take the sensors' data
	{
		$.ajax
		({

		 	url : urlAllMeasure + sensorType, //Target file in the server

		 	type : "GET",

		 	dataType : 'json', //We receive the data in JSON format

		 	success : displayMeasure,

		 	error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>"); //We send on the screen the table
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

		});	
	}
	else if(!$.isEmptyObject(xlast) && calendar == "%22:00%22") //If we have a limit for the number of data
	{
		$.ajax
		({
			
			url : urlLimit, //We send a request with the number of data that the user want

			type : "GET",

		 	dataType : 'json',

		 	success : displayMeasure,

		 	error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>"); //We send on the screen the table
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

		});	
	}
	else if($.isEmptyObject(xlast) && calendar != "%22:00%22") //If we have a limit of date
	{
		$.ajax	
		({
			
			url : urlDAte, //We send a request with the date from which we want the data

			type : "GET",

		 	dataType : 'json',

		 	success : displayMeasure,

		 	error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>"); //We send on the screen the table
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

		});			
	}

}






function getMeasuresForChart()
{
	var xlastChart = $("#xlastChart").val();

	sensorType = typeSensor();

	if(sensorType != "")
	{
		if(!$.isEmptyObject(xlastChart))
		{
			$.ajax //We send a GET request to draw the chart
			({
					
					url : urlAllMeasure + sensorType + urlLimitMeasure + xlastChart, // We send a request with the date from which we want the data

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
	else
	{
		$('#curve_chart').html("<p>Sorry, we don't have only one type of data, the draw is impossible</p>")
	}

}





function getUserCommand()
{

	$.ajax //We send a GET Request for take the user's commands
	({
			
			url : urlReadUserCommand, // We send a request with the date from which we want the data

			type : "GET",

		 	dataType : 'json',

		 	success : displayUserCommand,

		 	error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>"); //We send on the screen the table
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

	});

}


function getHardwareConfiguration()
{

	$.ajax //We send a GET Request for take the user's commands
	({
			
			url : urlHardwareConfiguration, // We send a request with the date from which we want the data

			type : "GET",

		 	dataType : 'json',

		 	success : displayHardwareConfiguration,

		 	error : function(resultat, statut, erreur)
		 	{
		 		if(resultat['status'] == '404')
		 		{
		 			$("#measure").html("<p>There is an error, the query found nothing</p>"); //We send on the screen the table
		 			console.log(resultat['status'] + " : " + erreur);
		 		}
		 	}

	});

}






/*
	This function draw a form to select the sensor data to display 
*/

function displayHardwareConfiguration(text)
{

	var data_long = text['hardwareConfigurations'].length; //We take the number of records in the form
	var name = '';
	var id = '';

	var txt_measures = ''; //We initiate the form to display

	txt_measures += '<input type="radio" name="sensor" value="" id="nothing" checked/> <label>"Nothing"</label><br />';

	for(i=0; i<data_long; i++) //We write in the string the data from the DB
	{

		id = text['hardwareConfigurations'][i]['id'];
		name = text['hardwareConfigurations'][i]['name'].split(" ");

		txt_measures += '<input type="radio" name="sensor" value="'+id+'" id="'+name[1]+'"/> <label>"'+name[1]+'"</label><br />';
	}

	$("#sensorTypeRequest").html(txt_measures); //We send on the screen the form
}







/*
	This function draw a table with the sensors' data 
*/

function displayMeasure(text)
{

	var data_long = text['measures'].length; //We take the number of records in the table

	var txt_measures = '<table id="measure_display"><th>Hardware Name</th><th>Value</th><th>TimeStamp</th>'; //We initiate the table to display

	for(i=0; i<data_long; i++) //We write in the string the data from the DB
	{
		var sens = text['measures'][i]['hardware_name'].split(" ");

		var typeSensor = sens[1];

		txt_measures += "<tr><td>" + typeSensor + "</td>"
		txt_measures += "<td>" + text['measures'][i]['value'] + "</td>"
		txt_measures += "<td>" + text['measures'][i]['timestamp'] + "</td></tr>"
	}
	txt_measures += "</table>";

	$("#measure").html(txt_measures); //We send on the screen the table

}

/*
	This function draw a table with the user's commands
*/

function displayUserCommand(text)
{

	var data_long = text['commandes'].length; //We take the number of records in the table

	var txt_userCommand = '<table id="userCommand_display"><th>Command</th><th>Target Name</th><th>Value</th><th>TimeStamp</th><th>Done</th>'; //We initiate the table to display

	for(i=0; i<data_long; i++) //We write in the string the data from the DB
	{
		txt_userCommand += "<tr><td>" + text['commandes'][i]['command'] + "</td>"
		txt_userCommand += "<td>" + text['commandes'][i]['name'] + "</td>"
		txt_userCommand += "<td>" + text['commandes'][i]['value'] + "</td>"
		txt_userCommand += "<td>" + text['commandes'][i]['timestamp'] + "</td>"
		txt_userCommand += "<td>" + text['commandes'][i]['done'] + "</td></tr>"
	}
	txt_userCommand += "</table>";

	$("#userCommand").html(txt_userCommand); //We send on the screen the table

}

/*
	This function send a request to the server to records a new user's command in the DB
*/

function postUserCommand()
{
	var type = $("#type").val(); //We take the command type in the HTML form

	var command = $("#command").val(); //We take the command type in the HTML form

	var targetName = $("#targetName").val(); //We take the command name type in the HTML form

	var val = $("#val").val(); //We take the command value type in the HTML form

	$.post(

		urlCreateUserCommand, //The target file on the server

		{ //The parameters of the request
			type : type,
			command : command,
			targetName : targetName,
			value : val
		},

		getUserCommand //the function that we want execute after the sends

	);
}

/*
	This function send a request to the server to records a new user's command in the DB
*/

function drawChart(text) 
{

	var data_long = text['measures'].length; //We take the number of records in the table

	var sens = text['measures'][0]['hardware_name'].split(" ");

	var typeSensor = sens[1];

	var increment = data_long - 1; //We initiate the increment variable

	var data = new google.visualization.DataTable(); //We create a new DataTable to draw the chart
	data.addColumn('number', 'Time'); //We ceate the first column
	data.addColumn('number', 'Order'); //We ceate the second column
	data.addColumn('number', typeSensor); //We ceate the third column

	var val = 0;
	var j = 0;

	if(!$.isEmptyObject(document.forms['orderRequest'].order.value))
	{
		order = document.forms['orderRequest'].order.value; //We take the regulation order in the HTML form
	}
	else
	{
		order = 10;
	}

	for(increment; increment>0; increment--)
	{
		val = text['measures'][increment]['value']; //We take the measure value in the request answer

		data.addRows([[j,parseFloat(order),parseFloat(val)]]); //We create a new row in the DataTable
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



    var chart = new google.visualization.LineChart(document.getElementById('curve_chart')); //We create a new chart

    chart.draw(data, options); //We draw the chart
}
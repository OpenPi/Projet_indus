var urlAllMeasure = '../measures/';
var urlLimitMeasure = '?xlast=';
var urlDateMeasure = '?time=';
var urlReadUserCommand = '../usercommands/';
var urlCreateUserCommand = '../usercommands/';

var order = 10;
var i = 0;
var sensorType = "";

setInterval(getMeasure, 1000); //Execute the get function each seconds
setInterval(getMeasuresForChart, 1000); //Execute the get function each seconds
setInterval(getUserCommand, 1000); //Execute the get function each seconds

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

	if($.isEmptyObject(xlast) && calendar == "%22:00%22") //if we don't have limits, we send a GET Request for take the sensors' data
	{
		$.get
		(

		 	urlAllMeasure + sensorType, //Target file in the server

		 	'', //We don't have arguments in the request

		 	displayMeasure, //When we have the server's answer, we execute this function

		 	'json' //We receive the data in JSON format

		);	
	}
	else if(!$.isEmptyObject(xlast) && calendar == "%22:00%22") //If we have a limit for the number of data
	{
		$.get
		(
			
			urlAllMeasure+ sensorType + urlLimitMeasure + xlast, //We send a request with the number of data that the user want

		 	'',

		 	displayMeasure,

		 	'json'

		);	
	}
	else if($.isEmptyObject(xlast) && calendar != "%22:00%22") //If we have a limit of date
	{
		$.get
		(
			
			urlAllMeasure+ sensorType + urlDateMeasure + calendar, //We send a request with the date from which we want the data

		 	'',

		 	displayMeasure,

		 	'json'

		);			
	}

}





function getMeasuresForChart()
{

	sensorType = typeSensor();

	$.get //We send a GET request to draw the chart
	(

	 	urlAllMeasure, // + sensorType,

	 	'',

	 	drawChart,

	 	'json'

	);

}





function getUserCommand()
{

	$.get //We send a GET Request for take the user's commands
	(

	 	urlReadUserCommand,

	 	'',

	 	displayUserCommand,

	 	'json'

	);

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
		txt_measures += "<tr><td>" + text['measures'][i]['hardwareName'] + "</td>"
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
		txt_userCommand += "<td>" + text['commandes'][i]['targetName'] + "</td>"
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
	var command = $("#command").val(); //We take the command type in the HTML form

	var targetName = $("#targetName").val(); //We take the command name type in the HTML form

	var val = $("#val").val(); //We take the command value type in the HTML form


	$.post(

		urlCreateUserCommand, //The target file on the server

		{ //The parameters of the request
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

	var increment = data_long - 1; //We initiate the increment variable

	var data = new google.visualization.DataTable(); //We create a new DataTable to draw the chart
	data.addColumn('number', 'Heure'); //We ceate the first column
	data.addColumn('number', 'Consigne'); //We ceate the second column
	data.addColumn('number', 'Temperature'); //We ceate the third column

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

		data.addRows([[j,parseInt(order),parseInt(val)]]); //We create a new row in the DataTable
		j++; 

	}

		//We create an option variable for the chart feature
        var options = {
          title: 'PID temperature',
          vAxis: {title: "Température"},
          hAxis: {title: "Heure"},
          curveType: 'function',
          legend: { position: 'bottom' }
        };



        var chart = new google.visualization.LineChart(document.getElementById('curve_chart')); //We create a new chart

        chart.draw(data, options); //We draw the chart
}
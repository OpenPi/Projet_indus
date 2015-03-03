var urlAllMeasure = 'measure/read.php';
var urlLimitMeasure = 'measure/read.php?xlast=';
var urlDateMeasure = 'measure/read.php?time=';
var urlReadUserCommand = 'userCommand/read.php';
var urlCreateUserCommand = 'userCommand/create.php';

var order = 10;
var i = 0;

setInterval(get, 1000); //Execute the get function each seconds

function get()
{

	var xlast = document.forms['xlastRequest'].xlast.value;

	var calendar = document.getElementById("timestamp").value;

	calendar = calendar.replace("T", "%20");
	calendar = calendar.replace("-", "/");
	calendar = calendar.replace("-", "/");
	calendar = "%22" + calendar + ":00%22";

	if($.isEmptyObject(xlast) && calendar == "%22:00%22") //if we don't have limits, we send a GET Request for take the sensors' data
	{
		$.get
		(

		 	urlAllMeasure, //Target file in the server

		 	'', //We don't have arguments in the request

		 	getMeasure, //When we have the server's answer, we execute this function

		 	'json' //We receive the data in JSON format

		);		
	}
	else if(!$.isEmptyObject(xlast) && calendar == "%22:00%22") //If we have a limit for the number of data
	{
		$.get
		(
			
			urlLimitMeasure + xlast, //We send a request with the number of data that the user want

		 	'',

		 	getMeasure,

		 	'json'

		);	
	}
	else if($.isEmptyObject(xlast) && calendar != "%22:00%22") //If we have a limit of date
	{
		$.get
		(
			
			urlDateMeasure + calendar, //We send a request with the date from which we want the data

		 	'',

		 	getMeasure,

		 	'json'

		);			
	}

	$.get //We send a GET request to draw the chart
	(

	 	urlAllMeasure,

	 	'',

	 	drawChart,

	 	'json'

	);	

	$.get //We send a GET Request for take the user's commands
	(

	 	urlReadUserCommand,

	 	'',

	 	getUserCommand,

	 	'json'

	);

}

/*
	This function draw a table with the sensors' data 
*/

function getMeasure(text)
{

	var data_long = text['measures'].length; //We take the number of records in the table


	var txt_measures = '<table id="measure_display"><th>Hardware Name</th><th>Value</th><th>TimeStamp</th>'; //We initiate the table to display

	for(i; i<data_long; i++) //We write in the string the data from the DB
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

function getUserCommand(text)
{

	var data_long = text['userCommands'].length; //We take the number of records in the table


	var txt_userCommand = '<table id="userCommand_display"><th>Command</th><th>Target Name</th><th>Value</th><th>TimeStamp</th><th>Done</th>'; //We initiate the table to display

	for(i; i<data_long; i++) //We write in the string the data from the DB
	{
		txt_userCommand += "<tr><td>" + text['userCommands'][i]['command'] + "</td>"
		txt_userCommand += "<td>" + text['userCommands'][i]['targetName'] + "</td>"
		txt_userCommand += "<td>" + text['userCommands'][i]['value'] + "</td>"
		txt_userCommand += "<td>" + text['userCommands'][i]['timestamp'] + "</td>"
		txt_userCommand += "<td>" + text['userCommands'][i]['done'] + "</td></tr>"
	}
	txt_userCommand += "</table>";

	$("#userCommand").html(txt_userCommand); //We send on the screen the table

}

/*
	This function send a request to the server to records a new user's command in the DB
*/

function postUserCommand()
{
	var command = document.forms['CreateUserCommand'].command.value; //We take the command type in the HTML form
	var targetName = document.forms['CreateUserCommand'].targetName.value; //We take the command name type in the HTML form
	var val = document.forms['CreateUserCommand'].val.value; //We take the command value type in the HTML form


	$.post(

		urlCreateUserCommand, //The target file on the server

		{ //The parameters of the request
			command : command,
			targetName : targetName,
			value : val
		},

		get //the function that we want execute after the sends

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
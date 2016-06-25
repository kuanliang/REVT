/*
	This script is customize highcharts options.
	Create By Kenny Chou, 2011-03-18
*/
var full_options = {
	chart: {
		renderTo: 'chart',
		animation: false,
		defaultSeriesType: 'spline',
		marginRight: 130,
		marginBottom: 50
	},
	credits:{
		enabled: false
	},
	title: {
		text: 'Test Serias'
	},
	xAxis:{
		title: {
			text:'Data information'
		}
	},
	yAxis:{
		max: 1,
		title: {
			text: 'Accuracy'
		},
	},
	legend:{
		layout: 'vertical',
		align: 'right',
		verticalAlign:'top',
	},
	plotOptions:{
		spline: {
			marker: {
				enabled: true,
				radius: 1
			},
			animation: false
		},
		line: {
			//color: '#00CC00',
			marker: {
				enabled: true,
				radius: 3,
				symbol: 'circle'
			},
			showInLegend: false,
			dataLabels:{
				enabled: true,
				formatter:function(){
					if(this.point.id=='end')
						return "<strong>"+this.series.name+"</strong>";
					else
						return ;
				}
			},
			animation: false
		},
		area:{
			color: '#CA9060',
			marker:{
				enabled: true,
				radius: 1,
				symbol: 'circle'
			},
			animation: false
		}
	},
	tooltip:{
		formatter: function(){
			if(this.series.name=="Accuracy")
				return "Data[<strong>"+this.x+"</strong>] Accuracy is <strong>"+ this.y+"</strong>";
			else if(this.series.name=="Entropy")
				return "Data[<strong>"+this.x+"</strong>] Entropy is <strong>"+ this.y+"</strong>";
			else if(this.series.type=="area")
				return this.x;
			else{
				if(this.point.id=='end')
					return "<strong>" + this.series.name+ "</strong>" +" end is from " + this.x;
				else
					return "<strong>" + this.series.name +"</strong>" +" start is from " + this.x;
			}
		}
	},
	series:[]
};

var class_options= {
	chart:{
		renderTo: '',
		defaultSeriesType: 'column',
	},
	title:{
		text: 'Class Accuracy'
	},
	xAxis:{
		categories: ['Domain','Plylum', 'Class', 'Order', 'Family', 'Genus'],
		title: {
			text: 'Class Value'
		}
	},
	yAxis:{
		max:1,
		title:{
			text: 'Accuracy'
		}
	},
	legend:{
		layout: 'vertical',
		align: 'right',
		verticalAlign:'top'
	},

	plotOptions: {
		column: {
			animation: false
		}
	},
	series:[]
};

var naive_options = {
	chart : {
		renderTo: '',
		defaultSeriesType: 'scatter',
	},
	credits:{
		enabled: false
	},
	title: {
		text: 'Bootstrap Chart Title'
	},
	xAxis: {
		title:{
			text: 'Bootstrap'
		}
	},
	yAxis:{
		max:1,
		title: {
			text: 'Accuracy'
		}
	},
	legend:{
		layout: 'vertical',
		align: 'right',
		verticalAlign:'top'
	},
	plotOptions: {
		scatter: {
			dataLabels:{
				enabled: true,
				formatter:function(){
					return "<strong>" +this.point.name +"</strong>";
				}
			}

		}
	},
	tooltip:{
		formatter: function(){
			return "<strong>" + 
					this.series.name + 
					": " +
					this.point.name +
					"</strong><br/>" +
					"Accuracy: " +this.point.y + 
					"<br/>" +
					"Bootstrap: "+ this.point.x
		}
	},

	series:[]
};

var primer_series = {
	type: 'line',
	name: '',
	data: [{
		x: 0,
		y: 0,
		marker:{
			enabled: false
		},
		id: 'start'
	},
	{
		x: 0,
		y: 0,
		id: 'end'
	}]
};

var vregion_series = {
	type: 'line',
	name: '',
	data: [{
		x: 0,
		y: 0,
		marker:{
			enabled: false
		},
		id: 'start'
	},{
		x: 0,
		y: 0,
		marker:{
			enabled: false
		},
		id: 'end'
	}]
};
var selection_options = {
	name: '',
	type: 'area',
	data: []
};
var naive_series = {
	name: '',
	data: [
		{x:0,y:0,name:'Domain'},
		{x:0,y:0,name:'Plylum'},
		{x:0,y:0,name:'Class'},
		{x:0,y:0,name:'Order'},
		{x:0,y:0,name:'Family'},
		{x:0,y:0,name:'Genus'}]
};

function clone(obj){
	if(obj == null || typeof(obj) != 'object')
		return obj;
	var temp = new obj.constructor(); 
	for(var key in obj)
		temp[key] = clone(obj[key]);
	return temp;
}
var table_options={
	chart:{
		renderTo: '',
		animation: false,
		defaultSeriesType: 'column'
	},
	credits:{ enabled: false},
	title:{text: ''},
	xAxis:{
		categories: [],
		title: {text: ''}
	},
	yAxis:{
		max:1,
		title: {text: ''}
	 },
	legend:{
		layout:'vertical',
		align: 'right',
		verticalAlign: 'middle'
	},
	series:[]
};
/*
	draw_plot(
		$data: data url;
		$plot-type: line or column;
		$div: div name;
		$caption: table Caption;
		$title: plot Title;
		$xtitle: plot X-Title;
		$ytitle: plot Y-Title;
		$desc: your description;

*/
function draw_plot($data, $plot_type, $div, $caption, $title, $xtitle, $ytitle, $desc){
	$.ajax({
		url: $data,
		dataType: 'json',
		error: function(){
			alert('format Error');
		},
		success: function(ret){
			var $divname=$("#"+$div);
			var $table=$div+"-table";
			var $plot=$div+"-plot";
			$divname.append('<div class="grid_5 alpha"><table id="'+$table+'"><caption>'+$caption+'</caption><thead><tr></tr></thead><tbody></tbody></table>'+$desc+'</div>');
			$("#"+$table+" thead tr:first").append("<th>&nbsp;</th>");
			for(i in ret.legend){
				$("#"+$table+" thead tr:first").append("<th>"+ret.legend[i]+"</th>");
			}

			for(i in ret.data){
				$("#"+$table).find("tbody").append($('<tr>')).end();
				$("#"+$table+" tbody tr:last").append("<th>"+ret.data[i].name+"</th>");
				for(j in ret.data[i].data)
					$("#"+$table+" tbody tr:last").append("<td title='"+ eval(ret.data[i].data[j]) +"'>"+ (eval(ret.data[i].data[j])*100).toFixed(2)+"</td");
			}
			$divname.append('<div id="'+$plot+'" class="grid_7 omega" style="height:250px;"></div>');
			var options = clone(table_options);
			options.chart.renderTo = $plot;
			options.chart.defaultSeriesType=$plot_type;
			options.xAxis.categories=ret.legend;
			options.title.text= $title;
			options.yAxis.title.text= $ytitle;
			for(i in ret.data)
				options.series.push(ret.data[i]);
			var chart = new Highcharts.Chart(options);

		}
	});
};

function draw_plot_table($data, $plot_type, $div, $caption, $title, $xtitle, $ytitle, $desc){
	$.ajax({
		url: $data,
		dataType: 'json',
		error: function(){
			alert('format Error');
		},
		success: function(ret){
			var $divname=$("#"+$div);
			var $table=$div+"-table";
			var $plot=$div+"-plot";
			$divname.append('<div class="grid_5 alpha"><table id="'+$table+'"><caption>'+$caption+'</caption><thead><tr></tr></thead><tbody></tbody></table>'+$desc+'</div>');
			$("#"+$table+" thead tr:first").append("<th>&nbsp;</th>");
			for(i in ret.legend){
				$("#"+$table+" thead tr:first").append("<th>"+ret.legend[i]+"</th>");
			}

			for(i in ret.data){
				$("#"+$table).find("tbody").append($('<tr>')).end();
				$("#"+$table+" tbody tr:last").append("<th>"+ret.data[i].name+"</th>");
				for(j in ret.data[i].data)
					$("#"+$table+" tbody tr:last").append("<td title='"+ eval(ret.data[i].data[j]) +"'>"+ (eval(ret.data[i].data[j])*100).toFixed(2)+"</td");
			}


		}
	});
};

function draw_plot_plot($data, $plot_type, $div, $caption, $title, $xtitle, $ytitle, $desc){
	$.ajax({
		url: $data,
		dataType: 'json',
		error: function(){
			alert('format Error');
		},
		success: function(ret){
			var $divname=$("#"+$div);
			var $table=$div+"-table";
			var $plot=$div+"-plot";
			$divname.append('<div id="'+$plot+'" class="grid_7 omega" style="height:250px;width:1000px"></div>');
			var options = clone(table_options);
			options.chart.renderTo = $plot;
			options.chart.defaultSeriesType=$plot_type;
			options.xAxis.categories=ret.legend;
			options.title.text= $title;
			options.yAxis.title.text= $ytitle;
			for(i in ret.data)
				options.series.push(ret.data[i]);
			var chart = new Highcharts.Chart(options);

		}
	});
};
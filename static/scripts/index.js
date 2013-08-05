/*
============
index.js
============
--------------------------------------------------------------------------
Name:		   index.js
Purpose:		Main Javascript Funciton for Mobile Check In admin.

Author:		 Zheng Li
Email:		 	ronnie.alonso@gmail.com

Created:		24 July 2013
Copyright:	  (c) Zheng Li 2013
--------------------------------------------------------------------------
*/
var content_title = ["学生信息" , "签到查询" , "签到规则" , 
						"签到时间统计" , "签到位置统计" , 
							"添加管理员" , "修改密码"]
var notification = ["查询的结果会在下表显示。点击右上角的叉即可关闭提醒。",
			"您可以在以下版块修改本学期学生报到的时间段，系统将会对在这段时间成功报到的学生进行记录。签到结果可以在-签到查询-中查询到并可将报到信息导出。"	,
			"下图为学生签到时间分布图：左图为以小时划分的统计图，右图为以月份划分的统计图",
			"以下为学生签到地理位置统计图，你可以查看指定时间段学生签到的位置分布",
			"请输入增加新增管理员的学号／工号，以此添加管理员；点击管理员信息中的叉来删除管理员。",
			"请你的输入新密码。点击右上角的叉即可关闭提醒。"]
var domain = window.location.protocol + '//' + window.location.host;

function CheckPsw(){
	var p=document.getElementById("psw1").value;
	if (ValidatePsw()){
		if(p.length==0){
				alert('请输入密码!');
				return false;
		 }
		var Expression=/^[A-Za-z0-9]+$/;
		var regExp=new RegExp(Expression);
		if(regExp.test(p)==false){
				alert('密码只能由数字和字母组成!');
				return false;
		}
		else if(p.length<6){
				alert('密码长度应大于6!');
				return false;
		}else{ 
			return true;
		}
	}
	else{return false;}
}
function ValidatePsw()
{
	var p1=document.getElementById("psw1").value;
	var p2=document.getElementById("psw2").value;
	if(p2.length==0)
	{
			alert('请输入确认密码');
			return false;
	}
	if(p1 != p2)
	{
			alert('两次输入密码不同,请重新输入');
			return false;
	}
	else{return true; }
}

function ischeckNum(num,op)
{
	if(num)
	{
		if(isNaN(num) && op == "option2")
		{
			alert('请输入的学号含有非数字');
			return false;
		}
		else
			return true;
		}
	else
	{
		alert('需输入内容');
		return false;
	}
}


function isDate(startDtVal , entDtVal){
	var stT = startDtVal.split("/");
	var enT = entDtVal.split("/");
	var date1=new Date();
	date1.setFullYear(Number(stT[2]),Number(stT[0]),Number(stT[1]));
	var date2=new Date();
	date2.setFullYear(Number(enT[2]),Number(enT[0]),Number(enT[1]));
	if(date1.valueOf()>date2.valueOf()){
		alert("开始日期不能大于结束日期！");
		return false;
	}
	return true;
}

function EditFunction(index,op){
		var xmlhttp;
		var uid,dt,notification;

		var result = $("#"+index);
		uid=result.find(".uid")[0].innerHTML;
		dt=result.find(".detect-time")[0].innerHTML;

		if(op==1){
			notification="你确定确认该次签到吗？";
		}
		else if(op==2){
			notification="你确定重置此用户吗？";
		}
		else if(op==3){
			notification="你确定删除此次验证吗？";
		}
		else
		{return;}
		var r=confirm(notification);
		if (r==false){return;}
		if (window.XMLHttpRequest){//e for IE7+, Firefox, Chrome, Opera, Safari
			xmlhttp=new XMLHttpRequest();
			}
		else{// code for IE6, IE5
			xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
			}

		xmlhttp.onreadystatechange=function(){
			if (xmlhttp.readyState==4 && xmlhttp.status==200){
				var resTex=xmlhttp.responseText;
				if (resTex=='0' && op==3){

						$("#" + index).hide(function(){$(this).remove();});
					}

				else if(resTex=='0' && op==2){
					alert("用户信息已重置！");

				}else if(resTex=='0' && op==1){
					alert("已经修改为成功签到！请手动刷新页面！");

				}
			}
		}
		url="/admin/student/edit?uid="+ uid + "&op="+ op+"&dt="+dt;
		xmlhttp.open("GET",url,true);
		xmlhttp.send();
}

function DeleteFunction(index){
		var xmlhttp;
		var uid;
		var result = $("#"+index);
		
		uid= result.find(".uid")[0].innerHTML;;

		var r=confirm("你确定要删除该管理员吗？");
		if (r==false){return;}
		if (window.XMLHttpRequest){//e for IE7+, Firefox, Chrome, Opera, Safari
			xmlhttp=new XMLHttpRequest();
			}
		else{// code for IE6, IE5
			xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
		}
		xmlhttp.onreadystatechange=function()
			{
			if (xmlhttp.readyState==4 && xmlhttp.status==200)
				{
					var resTex=xmlhttp.responseText;
					if (resTex=='0'){
						$("#" + index).hide(function(){$(this).remove();});
					}
					else {
						alert("删除管理员失败！")
						return false
					}
				}
			}
		url="/admin/manage/delete?uid="+uid;
		xmlhttp.open("GET",url,true);
		xmlhttp.send();
}

function ShowStudentInfo() {
	/* navigation */
	$(".nav-top-item").removeClass("current");

	$("#basic-nav").addClass("current");

	$(".current").not(".nav-top-item").removeClass("current");

	$("#student-tab").addClass("current");

	/* notification */
	$("#notification-banner").html(notification[0]);
	/* content box */
	$("#content-title").html(content_title[0]);

	// DISPLAY TEMPLATE
	$.get('/static/templates/student_tmpl.html', function(data) {
		$("#content-box-main").empty();		 

		$.template("student_tmpl", data);

		$.tmpl("student_tmpl", null).appendTo("#content-box-main");

		$("#search_submit").button();
		// $("#search_submit").css("height",30);

		$("#search_submit").bind('click' , function(argument) {
			var option = $("#search_type").val();
			var q = $("#search_key").val();
			if(ischeckNum(q,option)){
				var url = domain + '/admin/student?op=' + option + '&q=' + q;
				$.ajax({
					url: '/static/templates/stuinfo_tmpl.html',
					async:false,
					success:function(tmpl) {
							$.template("stuinfo_tmpl", tmpl);
					}
				});
				$.ajax({
					url:  url,
					dataType: 'json',
					async: true,
					success: function(data) {

						$("#table-body").empty();
						for (var i = 0; i < data.length; i++) {
							data[i].INDEX = i + 1;
							var doc = data[i];

							$.tmpl("stuinfo_tmpl", doc).appendTo("#table-body");
						}
					},			
					error:function(XMLResponse){alert(XMLResponse.responseText);}
				});
			}
		});
	});
}

function ShowCheckInfo() {
	$(".nav-top-item").removeClass("current");

	$("#basic-nav").addClass("current");

	$(".current").not(".nav-top-item").removeClass("current");

	$("#checkin-tab").addClass("current");

	/* notification */
	$("#notification-banner").html(notification[0]);

	/* content box */
	$("#content-title").html(content_title[1]);

	// DISPLAY TEMPLATE
	$.get('/static/templates/checkin_tmpl.html', function(data) {
		$("#content-box-main").empty();		 

		$.template("checkin_tmpl", data);

		$.tmpl("checkin_tmpl", null).appendTo("#content-box-main");

		$( "#datepicker1" ).datepicker();
		$( "#datepicker2" ).datepicker();

		$("#search_submit").button();
		$("#search_submit").bind('click' , function(argument) {
			var st = $("#datepicker1").val();
			var tm = $("#datepicker2").val();

			if(isDate(st,tm)){
				var url = domain + '/admin/checkin?start=' + st + '&terminal=' + tm;
				$.ajax({
					url: '/static/templates/chkinfo_tmpl.html',
					async:false,
					success:function(tmpl) {
							$.template("chkinfo_tmpl", tmpl);
					}
				});

				$.ajax({
					url:  url,
					dataType: 'json',
					async: true,
					success: function(data) {

						$("#table-body").empty();
						for (var i = 0; i < data.length; i++) {
							data[i].INDEX = i + 1;
							var doc = data[i];

							$.tmpl("chkinfo_tmpl", doc).appendTo("#table-body");
						}
					},			
					error:function(XMLResponse){alert(XMLResponse.responseText);}
				});
			}
		});

	});
}

function ModifyRule(){
	$(".nav-top-item").removeClass("current");

	$("#basic-nav").addClass("current");

	$(".current").not(".nav-top-item").removeClass("current");

	$("#rule-tab").addClass("current");

	/* content box */
	$("#content-title").html(content_title[2]);

	/* notification */
	$("#notification-banner").html(notification[1]);

	// DISPLAY TEMPLATE
	$.get('/static/templates/rule_tmpl.html', function(data) {
		$("#content-box-main").empty();		 

		$.template("rule_tmpl", data);

		var url = domain + '/admin/default_rule';

		$.ajax({
			url: url,
			async:false,
			success:function(doc) {
					$.tmpl("rule_tmpl", JSON.parse(doc)).appendTo("#content-box-main");

					$( "#datepicker1" ).datepicker();
					$( "#datepicker2" ).datepicker();
			
					$("#search_submit").button();
					$("#search_submit").bind('click' , function() {
						var st = $("#datepicker1").val();
						var tm = $("#datepicker2").val();
			
						if(isDate(st,tm)){
							var url = domain + '/admin/rule?start=' + st + '&terminal=' + tm;
							$.ajax({
								url:  url,
								dataType: 'json',
								async: true,
								success: function(data) {
										$("#start_time").html(st);
										$("#terminal_time").html(tm);
								},			
								error:function(XMLResponse){alert(XMLResponse.responseText);}
							});
						}
					});
			}
		});

	});
}

function ShowTimeStat () {
	$(".nav-top-item").removeClass("current");

	$("#stat-nav").addClass("current");

	$(".current").not(".nav-top-item").removeClass("current");

	$("#time-tab").addClass("current");

	/* notification */
	$("#notification-banner").html(notification[2]);

	/* content box */
	$("#content-title").html(content_title[3]);

	// DISPLAY TEMPLATE
	$.get('/static/templates/time_tmpl.html', function(data) {
		$("#content-box-main").empty();

		$.template("time_tmpl", data);

		$.tmpl("time_tmpl", null).appendTo("#content-box-main");

		QueryCoord(1,"stat");
		QueryCoord(2,"stat2");
		function QueryCoord(op,chart){
			var xmlhttp;
			if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
				xmlhttp=new XMLHttpRequest();
				}
			else{// code for IE6, IE5
				xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
				}
			xmlhttp.onreadystatechange=function(){
				if (xmlhttp.readyState==4 && xmlhttp.status==200){
						var resTex=xmlhttp.responseText;
						resTex=eval(resTex);
						var labels=[],data=[]
						for(var i=0; i<resTex.length; i++){
							labels.push(resTex[i].TIMES);
							data.push(resTex[i].NUMS);
						}
						var lineChartData = {
							labels:labels,datasets : [{
							fillColor : "rgba(220,220,220,0.5)",
							strokeColor : "rgba(220,220,220,1)",
							pointColor : "rgba(220,220,220,1)",
							pointStrokeColor : "#fff",
							data : data
						}]
				}
				var myLine = new Chart(document.getElementById(chart).getContext("2d")).Line(lineChartData);
				}
			}
			url="/admin/time_stat/"+op.toString();
			xmlhttp.open("GET",url,true);
			xmlhttp.send();
		}
	});
}

function ShowMapStat () {
	$(".nav-top-item").removeClass("current");

	$("#stat-nav").addClass("current");

	$(".current").not(".nav-top-item").removeClass("current");

	$("#map-tab").addClass("current");

	/* notification */
	$("#notification-banner").html(notification[3]);

	/* content box */
	$("#content-title").html(content_title[4]);

	// DISPLAY TEMPLATE
	$.get('/static/templates/map_tmpl.html', function(data) {
		$("#content-box-main").empty();

		$.template("map_tmpl.html", data);

		$.tmpl("map_tmpl.html", null).appendTo("#content-box-main");

		$( "#datepicker1" ).datepicker();
		$( "#datepicker2" ).datepicker();

		map = new GMaps({
			div: '#map',
			lat: 31.02444,
			lng: 121.436194,
			markerClusterer: function(map) {
				return new MarkerClusterer(map);
			}
		});

		function QueryCoord(){
			var xmlhttp;
			var start,terminal;
			start=document.getElementById("datepicker1").value;
			terminal=document.getElementById("datepicker2").value;
			if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
				xmlhttp=new XMLHttpRequest();
				}
			else{// code for IE6, IE5
				xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
				}
			xmlhttp.onreadystatechange=function(){
				if (xmlhttp.readyState==4 && xmlhttp.status==200){
						var resTex=xmlhttp.responseText;
						resTex=eval(resTex);
						map.removeMarkers();
			for(var i=0; i<resTex.length; i++){
							map.addMarker({
							lat: resTex[i].LATITUDE,
							lng: resTex[i].LONGITUDE,
							title: resTex[i].CHINAME,
							infoWindow: {
								content: '<p>'+resTex[i].CHINAME+'</p><br><p>签到时间：'+resTex[i].DETECTTIME+'</p>'
							}
						});
						}
				}
			}
			url="/admin/map_stat/search?start="+ start + "&terminal="+ terminal;
			xmlhttp.open("GET",url,true);
			xmlhttp.send();
		}

		$("#search_submit").button();
		$("#search_submit").bind("click" , function() {
			QueryCoord();
		})
	});	
}

function ManageAdmin(){
	$(".nav-top-item").removeClass("current");

	$("#admin-nav").addClass("current");

	$(".current").not(".nav-top-item").removeClass("current");

	$("#manage-tab").addClass("current");

	/* notification */
	$("#notification-banner").html(notification[4]);

	/* content box */
	$("#content-title").html(content_title[5]);

	// DISPLAY TEMPLATE
	$.get('/static/templates/admin_tmpl.html', function(data) {
		$("#content-box-main").empty();		 

		$.template("admin_tmpl", data);

		$.tmpl("admin_tmpl", null).appendTo("#content-box-main");


		$.ajax({
			url: '/static/templates/admininfo_tmpl.html',
			async:false,
			success:function(tmpl) {
					$.template("admininfo_tmpl", tmpl);

					var url = domain + '/admin/manage';
					$.ajax({
						url:  url,
						async: true,
						dataType:"json",
						success: function(data) {
							$("#table-body").empty();

							for (var i = 0; i < data.length; i++) {
								data[i].INDEX = i + 1;
								var doc = data[i];

								$.tmpl("admininfo_tmpl", doc).appendTo("#table-body");
							}
						},			
						error:function(XMLResponse){alert(XMLResponse.responseText);}
					});
			}
		});


		$("#search_submit").button();
		$("#search_submit").bind('click' , function(argument) {
			var snum = $("#StuId").val();
			if(ischeckNum(snum , "option2")){
				var url = domain + '/admin/addadmin?number=' + snum;
				$.ajax({
					url:  url,
					async: true,
					success: function(data) {

					},			
					error:function(XMLResponse){alert(XMLResponse.responseText);}
				});
			}
		});

	});
}

function PswSetting(){
	$(".nav-top-item").removeClass("current");

	$("#admin-nav").addClass("current");

	$(".current").not(".nav-top-item").removeClass("current");

	$("#setting-tab").addClass("current");

	/* notification */
	$("#notification-banner").html(notification[5]);

	/* content box */
	$("#content-title").html(content_title[6]);

	// DISPLAY TEMPLATE
	$.get('/static/templates/setting_tmpl.html', function(data) {
		$("#content-box-main").empty();		 

		$.template("setting_tmpl", data);

		$.tmpl("setting_tmpl", null).appendTo("#content-box-main");

		$("#search_submit").button();

		$("#search_submit").bind('click',function(){

			if(CheckPsw()){
				var psw1 = $("#psw1").val();
				var url = domain + '/admin/setting?psw1=' + psw1;
	
				$.ajax({
					url: url,
					async:false,
					success:function(doc) {
						$("#psw_msg").html(doc);
					}
				});
			}
		});
			
	});
}

$(document).ready(function(){
/* =============================================== */

/* =======   simpla jquery configuration  =========*/

/* =============================================== */
	//Sidebar Accordion Menu:
	$("#main-nav li ul").hide(); // Hide all sub menus
	$("#main-nav li a.current").parent().find("ul").slideToggle("slow"); // Slide down the current menu item's sub menu
	
	$("#main-nav li a.nav-top-item").click( // When a top menu item is clicked...
		function () {
			$(this).parent().siblings().find("ul").slideUp("normal"); // Slide up all sub menus except the one clicked
			$(this).next().slideToggle("normal"); // Slide down the clicked sub menu
			return false;
		}
	);
	
	$("#main-nav li a.no-submenu").click( // When a menu item with no sub menu is clicked...
		function () {
			window.location.href=(this.href); // Just open the link instead of a sub menu
			return false;
		}
	); 

	// Sidebar Accordion Menu Hover Effect:
	$("#main-nav li .nav-top-item").hover(
		function () {
			$(this).stop().animate({ paddingRight: "25px" }, 200);
		}, 
		function () {
			$(this).stop().animate({ paddingRight: "15px" });
		}
	);

	//Minimize Content Box
	$(".content-box-header h3").css({ "cursor":"s-resize" }); // Give the h3 in Content Box Header a different cursor
	$(".closed-box .content-box-content").hide(); // Hide the content of the header if it has the class "closed"
	$(".closed-box .content-box-tabs").hide(); // Hide the tabs in the header if it has the class "closed"
	
	$(".content-box-header h3").click( // When the h3 is clicked...
		function () {
		  $(this).parent().next().toggle(); // Toggle the Content Box
		  $(this).parent().parent().toggleClass("closed-box"); // Toggle the class "closed-box" on the content box
		  $(this).parent().find(".content-box-tabs").toggle(); // Toggle the tabs
		}
	);

	// Content box tabs:
	$('.content-box .content-box-content div.tab-content').hide(); // Hide the content divs
	$('ul.content-box-tabs li a.default-tab').addClass('current'); // Add the class "current" to the default tab
	$('.content-box-content div.default-tab').show(); // Show the div with class "default-tab"
	
	$('.content-box ul.content-box-tabs li a').click( // When a tab is clicked...
		function() { 
			$(this).parent().siblings().find("a").removeClass('current'); // Remove "current" class from all tabs
			$(this).addClass('current'); // Add class "current" to clicked tab
			var currentTab = $(this).attr('href'); // Set variable "currentTab" to the value of href of clicked tab
			$(currentTab).siblings().hide(); // Hide all content divs
			$(currentTab).show(); // Show the content div with the id equal to the id of clicked tab
			return false; 
		}
	);

	//Close button:
	$(".close").click(
		function () {
			$(this).parent().fadeTo(400, 0, function () { // Links with the class "close" will close parent
				$(this).slideUp(400);
			});
			return false;
		}
	);

	// Alternating table rows:
	$('tbody tr:even').addClass("alt-row"); // Add class "alt-row" to even table rows

	// Check all checkboxes when the one in a table head is checked:
	$('.check-all').click(
		function(){
			$(this).parent().parent().parent().parent().find("input[type='checkbox']").attr('checked', $(this).is(':checked'));   
		}
	);

	// Initialise jQuery WYSIWYG:
	$(".wysiwyg").wysiwyg(); // Applies WYSIWYG editor to any textarea with the class "wysiwyg"


/* =============================================== */

/* ================= index AJAX  =================*/

/* =============================================== */

	ShowStudentInfo();

	/* Setting navigation button*/
	$("#student-tab").bind("click", function() {
		if(!$(this).hasClass("current")){
			ShowStudentInfo();
		}
	});

	$("#checkin-tab").bind("click", function() {
		if(!$(this).hasClass("current")){
			ShowCheckInfo();
		}
	});

	$("#rule-tab").bind("click", function() {
		if(!$(this).hasClass("current")){
			ModifyRule();
		}
	});

	$("#time-tab").bind("click", function() {
		if(!$(this).hasClass("current")){
			ShowTimeStat();
		}
	});

	$("#map-tab").bind("click", function() {
		if(!$(this).hasClass("current")){
			ShowMapStat();
		}
	});

	$("#manage-tab").bind("click", function() {
		if(!$(this).hasClass("current")){
			ManageAdmin();
		}
	});

	$("#setting-tab").bind("click", function() {
		if(!$(this).hasClass("current")){
			PswSetting();
		}
	});
})

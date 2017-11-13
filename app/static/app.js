// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );


});

var primero = {};


function fblogin() {    	    
	console.log('Quieres iniciar sesion');
	FB.login(function(response) {
	   statusChangeCallback(response);
	},{scope: 'public_profile,email,user_photos,user_posts'}); 
}




//Load albums of user
function fbupload(){
	console.log('Abriste los albumes');
	FB.api(
	  '/me',
	  'GET',
	  {"fields":"albums.limit(999)"},
	  function(response) {
	  	console.log(response);
	  	var albums = response.albums.data;
	  	// var minimo = new Date(Math.max.apply(Math, albums.map(function(item){
	  	// 	console.log(new Date(item.created_time));
	  	// 	return item.created_time;})));
	  	// console.log(minimo);
	  	albums.sort(function(a, b) { 
	  		return parseFloat(a.id) - parseFloat(b.id); 
	  	});
	  	console.log(albums);
	  	console.log(albums[0]);
	  	var date_inicio = albums[0].created_time;
	  	getfirstpost(date_inicio);

	});
}


//Load last post
function getfirstpost(date){
	console.log('voy por el post ahora si');
	date = new Date(date);
	date_since = new Date(date);
	date_until = new Date(date);
	console.log(date_since);
	console.log(date_until);
	// var fecha = date.getFullYear()+'-' + (date.getMonth()+1) + '-'+date.getDate();//prints expected format.
	// Since
	date_since.setFullYear(date_since.getFullYear()-1);
	console.log(date_since);
	// until
	date_until.setMonth(date_until.getMonth()+1);
	console.log(date_until);
	// console.log(fecha);
	var url = "/me/feed?limit999&since="+date_since.toUTCString()+"&until="+date_until.toUTCString();
	FB.api(
	  url,
	  'GET',
	  function(response) {
	  	console.log(response);
	  	var posteos = response.data;
	  	posteos.sort(function(a,b){
	  		return parseFloat(a.created_time) - parseFloat(b.created_time);
	  	}).reverse();

	  		


	  	var f = function(i){
	  		if (i >= posteos.length) return;
	  		console.log(posteos[i].id);
	  		getPostData(posteos[i].id, function(mensaje){
		  		if(mensaje){
		  			console.log(mensaje);
		  			console.log('este es el mensaje más viejo: ', mensaje[0].message);
		  			primero['message']=mensaje[0].message;
		  			primero['link_post']=mensaje[0].link;
		  			primero['nombre']=mensaje[0].nombre;
		  			console.log('guardé mensaje en array');
		  			console.log(mensaje[0].imagen);
		  			getImage(mensaje[0].imagen);

		  			
		  		} else{
		  			console.log('no hay mensaje en este post');
		  			f(i+1);
		  		}
		  	});
		}
		f(0);	  
	});
}

function getPostData(id, callback){
	FB.api(
	    "/"+id,
	    'GET',
		{"fields":"message, object_id, picture, link, permalink_url"},
	    function (response) {
			console.log(response);
			if (response.message) {
				var mensaje = new Array();
				console.log(response.message);
				console.log(response.object_id);
				console.log(response.permalink_url);
				mensaje.push({"message":response.message,"imagen":response.object_id,"link":response.permalink_url,"nombre":response.name});
				callback(mensaje);
	        } else{
	        	callback(false);
	        }
	    }
	);
}

function getImage(img){
	FB.api(
		  "/"+img,
		  'GET',
		  {"fields":"link,picture"},
		  function(response) {
		  	console.log(response.link);
		  	console.log(response.picture);
		  	primero['link']=response.link;
		  	primero['image']=response.picture;
		  	console.log(primero);
		  	console.log(JSON.stringify(primero));
		 	//  	$.getJSON( '/post', { 'thing' : 'valor' } , function( data ) {
			//     //do stuff with data
			//     console.log(data);
			// });

		  	$.ajax({
			    url: $SCRIPT_ROOT + "/post",
			    type: "POST",
			    data: JSON.stringify(primero),
			    contentType: "application/json",
			    success: function(dat) {
			    	console.log('logré exportar el primero'); 
			    	// window.location.href = "http://localhost:5000/post";
			    	console.log(dat);
			    	window.location.href = $SCRIPT_ROOT + "/post";
			    },
			    error: function (err){
			    	console.log(err);
			    }
			});
			
			// $.post("/post",primero,function(data,status)
   //          {
   //              var tmp = data;            
   //              console.log(data.otstr);                     

   //          });
		  	
		  });
}


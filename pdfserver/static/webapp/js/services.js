"use strict";
var services = angular.module('services', ['ngResource']);

var SAVE_DATA_ENDPOINT = "http://testclimaterealty.appspot.com/v1/save/";
if (window.location.href.indexOf("localhost") !== -1){
  SAVE_DATA_ENDPOINT =  "http://localhost:5005/v1/save/";
}

var QUESTION_ENDPOINT = "http://testclimaterealty.appspot.com/v1/questions/";
if (window.location.href.indexOf("localhost") !== -1){
  QUESTION_ENDPOINT =  "http://localhost:5005/v1/questions/";
}

var ANALYZE_ENDPOINT = "http://clr.adaptinfrastructure.com/proto4/analyze_asset_api/";
if (window.location.href.indexOf("localhost") !== -1){
  //alert("We are on localhost. Will use Django server running on port 9000");
  ANALYZE_ENDPOINT = "http://localhost:9000/proto4/analyze_asset_api/";
}

var AVAILABLE_SLR_MODELS_ENDPOINT = "http://clr.adaptinfrastructure.com/proto4/available_sea_level_rise_models_api/";
if (window.location.href.indexOf("localhost") !== -1){
  //alert("We are on localhost. Will use Django server running on port 9000");
  AVAILABLE_SLR_MODELS_ENDPOINT = "http://localhost:9000/proto4/available_sea_level_rise_models_api/";
}


services.factory('QUESTIONS', ['$resource', function($resource){
  return $resource(QUESTION_ENDPOINT,{},{
      'save': {
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
      },
  } );
}]);

services.factory('SAVER', ['$resource', function($resource){
  return $resource(SAVE_DATA_ENDPOINT,{},{
      'save': {
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
      },
  } );
}]);



var ELEVATION_LIDAR_ENDPOINT = "http://elevation.adaptinfrastructure.com/elevation/lat/:lat/lng/:lng";

services.factory('ANALYZER', ['$resource', function($resource){
  return $resource(ANALYZE_ENDPOINT,{},{
      'analyze': {
        method: 'POST',
        headers: { 'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8' },
      },
  } );
}]);

services.factory('AVAILABLE_SLR_MODELS', ['$resource', function($resource){
  return $resource(AVAILABLE_SLR_MODELS_ENDPOINT,{},{
      'get': {
        method: 'POST',
        headers: { 'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8' },
      },
  } );
}]);

services.factory('ELEVATION_LIDAR', ['$resource', function($resource){
  return $resource(ELEVATION_LIDAR_ENDPOINT,{lat:'@lat', lng:'@lng'},{
      'get': {
        method: 'GET',
        headers: { 'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8' },
      },
  } );
}]);


// Google async initializer needs global function, so we use $window
services.factory('INITIALIZER', function($window, $q){

    //Google's url for async maps initialization accepting callback function
    var asyncUrl='https://maps.googleapis.com/maps/api/js?key=AIzaSyD61SGXvjz8rckhOmo_xR6im669wHfqubM&signed_in=true&callback=';
    //var asyncUrl = 'https://maps.googleapis.com/maps/api/js?callback=',
    var mapsDefer = $q.defer();

    //Callback function - resolving promise after maps successfully loaded
    $window.googleMapsInitialized = mapsDefer.resolve; // removed ()

    //Async loader
    var asyncLoad = function(asyncUrl, callbackName) {
    var script = document.createElement('script');
    //script.type = 'text/javascript';
    script.src = asyncUrl + callbackName;
    document.body.appendChild(script);
    };
    //Start loading google maps
    asyncLoad(asyncUrl, 'googleMapsInitialized');

    //Usage: Initializer.mapsInitialized.then(callback)
    return {
mapsInitialized : mapsDefer.promise
    };
})


var kumbayaModule = angular.module('kumbaya', [
  'ui.router'
]);


kumbayaModule

.run(
  ['$rootScope', '$state', '$stateParams',
    function ($rootScope,   $state,   $stateParams) {
      $rootScope.$state = $state;
      $rootScope.$stateParams = $stateParams;
    }
  ]
)

.config(
  ['$stateProvider', '$urlRouterProvider',
    function ($stateProvider,   $urlRouterProvider) {

    //// Redirects and Invalid URLs ////

      $urlRouterProvider

        // If the url is ever the 1st param, then redirect to the 2nd param
        .when('/c?id', '/contacts/:id')
        .when('/user/:id', '/contacts/:id')

        // Redirect invalid URLs to '/'
        .otherwise('/');


    //// State Configurations ////

      $stateProvider

        // Home
        .state("home", {
          url: "/",
          templateUrl: 'app/partials/testpartial.html',
          controller: "HomeController"
        })

    }
  ]
);

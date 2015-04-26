angular.module('ionicApp', ['ionic'])

.config(function($stateProvider, $urlRouterProvider) {

  $stateProvider
  .state('intro', {
    url: '/',
    templateUrl: 'templates/intro.html',
    controller: 'IntroCtrl'
  })
  .state('page9', {
    url: '/createroom',
    templateUrl: 'page9.html'
  })
        
  .state('page10', {
         url: '/waiting',
         templateUrl: 'page10.html'
         })

  .state('page11', {
         url: '/findaroom',
         templateUrl: 'page11.html'
         })
   .state('page12', {
      url: '/nightmafia',
      templateUrl: 'page12.html'
    })
    
    .state('page13', {
      url: '/nightcivilian',
      templateUrl: 'page13.html'
    })
    
    .state('page14', {
      url: '/day',
      templateUrl: 'page14.html'
    })
    
    .state('page15', {
      url: '/vote',
      templateUrl: 'page15.html'
    })
    
    .state('page16', {
      url: '/execute',
      templateUrl: 'page16.html'
    })
    
    .state('page17', {
      url: '/page17',
      templateUrl: 'page17.html'
    })
    
    .state('page18', {
      url: '/page18',
      templateUrl: 'page18.html'
    })
    
    .state('page19', {
      url: '/page19',
      templateUrl: 'page19.html'
    })
  .state('main', {
    url: '/main',
    templateUrl: 'templates/main.html',
    controller: 'MainCtrl'
  });

  $urlRouterProvider.otherwise("/");

})

.controller('IntroCtrl', function($scope, $state, $ionicSlideBoxDelegate) {
 
  // Called to navigate to the main app
  $scope.startApp = function() {
    $state.go('main');
  };
  $scope.next = function() {
    $ionicSlideBoxDelegate.next();
  };
  $scope.previous = function() {
    $ionicSlideBoxDelegate.previous();
  };

  // Called each time the slide changes
  $scope.slideChanged = function(index) {
    $scope.slideIndex = index;
  };
})

.controller('MainCtrl', function($scope, $state) {
  console.log('MainCtrl');
  
  $scope.toIntro = function(){
    $state.go('main');
  }
});





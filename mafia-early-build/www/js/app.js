angular.module('app', ['ionic'])

.run(function($ionicPlatform) {
     $ionicPlatform.ready(function() {
                          // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
                          // for form inputs)
                          if(window.cordova && window.cordova.plugins.Keyboard) {
                          cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
                          }
                          if(window.StatusBar) {
                          // org.apache.cordova.statusbar required
                          StatusBar.styleDefault();
                          }
                          });
     })

.config(function($stateProvider, $urlRouterProvider) {
        
        // Ionic uses AngularUI Router which uses the concept of states
        // Learn more here: https://github.com/angular-ui/ui-router
        // Set up the various states which the app can be in.
        // Each state's controller can be found in controllers.js
        $stateProvider
        .state('intro', {
               url: '/',
               templateUrl: 'intro.html',
               //controller: 'IntroCtrl'
               })
//        .state('main', {
//               url: '/main',
//               templateUrl: 'main.html',
//               //controller: 'MainCtrl'
//               });
//

        .state('page8', {
               url: '/main',
               templateUrl: 'page8.html'
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
               url: '/intro',
               templateUrl: 'page12.html'
               })
        ;
        
        // if none of the above states are matched, use this as the fallback
        
        $urlRouterProvider.otherwise('/main');
        
        
        });
//    .controller('IntroCtrl', function($scope, $state, $ionicSlideBoxDelegate) {
//            
//            // Called to navigate to the main app
//            $scope.startApp = function() {
//            $state.go('main');
//            };
//            $scope.next = function() {
//            $ionicSlideBoxDelegate.next();
//            };
//            $scope.previous = function() {
//            $ionicSlideBoxDelegate.previous();
//            };
//            
//            // Called each time the slide changes
//            $scope.slideChanged = function(index) {
//            $scope.slideIndex = index;
//            };
//            })
//
//    .controller('MainCtrl', function($scope, $state) {
//            console.log('MainCtrl');
//            
//            $scope.toIntro = function(){
//            $state.go('page8');
//            }
//            });

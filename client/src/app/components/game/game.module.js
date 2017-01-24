
/**
 *
 * @ngdoc module
 * @name components
 *
 * @requires components.contact
 * @requires components.auth
 *
 * @description
 *
 * This is the components module. It includes all of our components.
 *
 **/

angular
	.module('app.components.game', [
		'ui.select'
	])
	.config(function($stateProvider) {
		$stateProvider
			.state('game', {
				url: '/game',
				template: '<div ui-view></div>'
			});
	});
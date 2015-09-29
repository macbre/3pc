var assert = require('assert'),
	thirdParty = require('./');

describe('3pc', function () {
	it('should provide an API', function() {
		assert(typeof thirdParty === 'object');
	});

	it('should expose raw database objects', function() {
		assert(typeof thirdParty.db === 'object');
		assert(typeof thirdParty.db.cdn === 'object');
		assert(typeof thirdParty.db.trackers === 'object');
	});
});


var assert = require('assert'),
	leche = require('leche'),
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

describe('3pc CDN', function() {
	it('should detect CDN provider properly', function() {
		leche.withData([
			[
				'http://example.com/Foo',
				false
			],
			// match domains only
			[
				'http://example.com/foo.google.js',
				false
			],
			// Fastly
			[
				'http://vignette3.wikia.nocookie.net/nordycka/images/e/ee/Tj%C3%B8rnuv%C3%ADk.jpg/revision/latest/scale-to-width-down/640?cb=20150904165805&path-prefix=pl',
				'Fastly'
			],
			// Google
			[
				'https://lh5.googleusercontent.com/-FAXbnxo1usQ/AAAAAAAAAAI/AAAAAAAAAF0/jOm0yGSWlc0/photo.jpg?sz=104',
				'Google'
			],
			[
				'http://googlehosted.com/foo.js',
				'Google'
			]
		], function(url, expected) {
			assert.equal(thirdParty.cdn.matchByUrl(url), expected, url + ' should be provided by ' + expected);
		});
	});
});


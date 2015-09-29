var fs = require('fs'),
	urlParse = require('url').parse;

// export "raw" databases
var db = {};

['cdn', 'trackers'].forEach(function(dbName) {
	var fileName = __dirname + '/db/' + dbName + '.json';
	db[dbName] = JSON.parse(fs.readFileSync(fileName));
});

// matchers
function _find_match(haystack, needle, callback) {
	var ret = false;

	Object.keys(haystack).forEach(function(entry) {
		if (callback(needle, entry) === true) {
			ret = haystack[entry];
			return false;
		}
	});

	return ret;
}

function cdnMatchByUrl(url) {
	var domain = urlParse(url)['hostname'];

	// match by strpos()
	return _find_match(db.cdn['by_domain'], domain, function(needle, entry) {
		return needle.indexOf(entry) > -1;
	});
}

function trackersMatchByUrl(url) {
	// match by strpos()
	var ret = _find_match(db.trackers['by_url'], url, function(needle, entry) {
		return needle.indexOf(entry) > -1;
	});

	if (ret !== false) {
		return ret;
	}

	// match by regex
	return _find_match(db.trackers['by_regexp'], url, function(needle, entry) {
		var re = new RegExp(entry);
		return re.test(needle) === true;
	});
}

// module's public API
module.exports = {
	db: db,
	cdn: {
		matchByUrl: cdnMatchByUrl
	},
	trackers: {
		matchByUrl: trackersMatchByUrl
	}
};


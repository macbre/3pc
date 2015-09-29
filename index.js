var fs = require('fs'),
	urlParse = require('url').parse;

// export "raw" databases
var db = {};

['cdn', 'trackers'].forEach(function(dbName) {
	var fileName = __dirname + '/db/' + dbName + '.json';
	db[dbName] = JSON.parse(fs.readFileSync(fileName));
});

// matchers
function cdnMatchByUrl(url) {
	var domain,
		domains = db.cdn['by_domain'],
		ret = false

	// parse the URL
	domain = urlParse(url)['hostname'];

	// try to find a match
	Object.keys(domains).forEach(function(entry) {
		if (domain.indexOf(entry) > -1) {
			ret = domains[entry];
			return false;
		}
	});

	return ret;
}

// module's public API
module.exports = {
	db: db,
	cdn: {
		matchByUrl: cdnMatchByUrl
	}
};


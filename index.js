var fs = require('fs');

// export "raw" databases
var db = {};

['cdn', 'trackers'].forEach(function(dbName) {
	var fileName = __dirname + '/db/' + dbName + '.json';
	db[dbName] = JSON.parse(fs.readFileSync(fileName));
});

// module's public API
module.exports = {
	db: db
};


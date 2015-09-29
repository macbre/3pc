3pc
===

Third party web content database

## What is it?

`3pc` is meant to be a data-provider of CDN and 3rd party tracking services list.

Inspired by [this PerfPlanet article](http://calendar.perfplanet.com/2013/thirdpartycontent/).

## Usage

`3pc` is built as nodejs module:

```
npm install 3pc
```

It provides "raw" data and some helper functions:

```js
var thirdParty = require('3pc');

// check if given URL is provided via Content Delivery Network
console.log(thirdParty.cdn.matchByUrl('http://example.com/foo.js'));
false

console.log(thirdParty.cdn.matchByUrl('http://vignette3.wikia.nocookie.net/nordycka/images/e/ee/Tj%C3%B8rnuv%C3%ADk.jpg/revision/latest/scale-to-width-down/640?cb=20150904165805&path-prefix=pl'));
Fastly

// check if given URL is not a tracking code
console.log(thirdParty.trackers.matchByUrl('http://edge.quantserve.com/quant.js'));
Quantcast
```

## Data sources

`3pc` is currently using the following data sources:

* [CDN providers from webpagetest](https://raw.githubusercontent.com/WPO-Foundation/webpagetest/master/agent/wpthook/cdn.h)
* [Tracking tools from Ghostery](https://raw.githubusercontent.com/jonpierce/ghostery/master/firefox/ghostery-statusbar/ghostery/chrome/content/ghostery-bugs.js)

These sources are parsed and the result is stored in `./db` directory by running a Python script:

```
make generate
```

So this database can be used by any technology that can read and parse JSON-encoded files.

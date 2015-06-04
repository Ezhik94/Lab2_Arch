importScripts('parser.js');

self.addEventListener('message', function(e) {
    self.postMessage(e.data[3]);
    var expr = Parser.parse(e.data[3]);
    var u = Math.random();
    var x = parseFloat(e.data[0]) + (parseFloat(e.data[1]) - parseFloat([e.data[0]]))*u;

    var data = {
        x: 0
    };

    data.x = x;
    var Result = expr.evaluate(data);
    self.postMessage(Result);

}, false);
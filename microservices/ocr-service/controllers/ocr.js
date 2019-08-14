const { PythonShell } = require('python-shell');

const Ocr = module.exports;
// TODO : Update later
// const OcrDB = require('../models/bet');
Ocr.extractInfoFromRaidImage = async () => {

    img = '1.jpg'

    let pyshell = new PythonShell('./ocr-python/main.py', {
        args: ['-i', img]
    });

    pyshell.on('message', function (message) {
        console.log(message);
    });

    pyshell.end(function (err, code, signal) {
        if (err) throw err;
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
    });
}

Ocr.runTestsExtractInfoFromRaidImage = async () => {

    let pyshell = new PythonShell('./ocr-python/main.py', { args: '-t' });

    pyshell.on('message', function (message) {
        console.log(message);
    });

    pyshell.end(function (err, code, signal) {
        if (err) throw err;
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
    });
}
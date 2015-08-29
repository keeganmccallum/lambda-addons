var express = require('express');
var router = express.Router();

var PythonShell = require('python-shell');


/* GET home page. */
router.get('/', function(req, res, next) {
  var action = req.query.action,
      data = req.query.data,
      pyshell = new PythonShell('../../test_list.py', {mode: 'json'});

  if (!action) {
    res.render("index", {data: {}});
    return;
  }
  try{
    data = JSON.parse(data);
  } catch(e) {

  }
  // console.log(data)
  // console.log(JSON.stringify({action: action, data: data}))
  pyshell.send({action: action, data: data});
  pyshell.on('message', function (message) {
    res.render("index", {data: message});
    // end the input stream and allow the process to exit
  });
  pyshell.end(function (err) {
    if (err) res.status(500);
  });
});

module.exports = router;

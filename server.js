/* import Modules */
const http = require('http')
const express = require('express')
const mysql = require('mysql')
const createError = require('http-error')

/* connect to the database */
const dbconfig = require('./config/db.js')
//const conn = mysql.createConnection(dbconfig)

const bodyParser = require('body-parser')
app.use(bodyParser.urlencoded({
  extended: false
}))

app.use(bodyParser.json())
app.use(express.static('public'))

app.post('/data', (req, res) => {
  /* status, value */
  const data = req.body.status
  const value = req.body.value

  //implements here

  res.send()
})

app.use((error, res, next) => {
  next(createError(404))
})

app.set('port', process.env.PORT || 52275)
app.listen(app.get('port'), () => {
  console.log('NODE EXPRESS SERVER listening on port ' + app.get('port'));
})

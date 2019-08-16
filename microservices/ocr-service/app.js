const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const cors = require('cors');
const axios = require('axios');
const ocrRouter = require('./routes/ocr');

const app = express();

// Testing
const ocrController = require('./controllers/ocr')

require('dotenv').config();

app.use(cors())
app.options('*', cors())

// Read defined hosts
global.MS_USERS = process.env.MS_USERS || ''

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', ocrRouter);


module.exports = app;

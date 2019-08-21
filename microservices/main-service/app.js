const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const cors = require('cors');

const gymRouter = require('./routes/gym');

const app = express();

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

app.use('/gym', gymRouter);

module.exports = app;

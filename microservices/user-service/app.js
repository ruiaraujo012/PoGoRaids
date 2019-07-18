const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const passport = require('passport');
const cors = require('cors');

const indexRouter = require('./routes/index');
const userRouter = require('./routes/user');

const app = express();

require('dotenv').config();
require('./auth/auth');

app.use(cors())
app.options('*', cors())

app.use(passport.initialize());

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/user', userRouter);


module.exports = app;

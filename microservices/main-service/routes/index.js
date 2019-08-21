const express = require('express');
const router = express.Router();

const dbRaid = require('../models/raid');
const dbGym = require('../models/gym');

router.get('/ping', async (req, res, next) => {
    dbRaid.create({ name: 'Braga Parque 123' })
    res.send('Answering from main service');
})


module.exports = router;

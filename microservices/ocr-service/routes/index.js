const express = require('express');
const router = express.Router();
const Ocr = require('../controllers/ocr');

router.get('/ping', async (req, res, next) => {
    Ocr.extractInfoFromRaidImage()
    res.send('Answering from ocr service');
})


module.exports = router;

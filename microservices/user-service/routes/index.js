const express = require('express');
const router = express.Router();

router.get('/ping', (req, res, next) => {
    res.send('Answering from User Service');
})

module.exports = router;

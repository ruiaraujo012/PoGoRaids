const express = require('express');
const router = express.Router();

router.get('/ping', async (req, res, next) => {
    res.send('Answering from generic service');
})


module.exports = router;

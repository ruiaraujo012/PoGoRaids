const express = require('express');
const router = express.Router();
const Ocr = require('../controllers/ocr');

router.get('/extract/:id', async (req, res, next) => {

    pyshell = await Ocr.extractInfoFromRaidImage(`${req.params.id}.jpg`)
    console.log("Printing extracted info");
    await pyshell.on('message', (message) => {
        console.log("Triggering")
        extractedInfo = message;
        console.log(message);

        res.send(extractedInfo)
    });

})


module.exports = router;

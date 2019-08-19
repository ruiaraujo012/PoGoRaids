const express = require('express');
const router = express.Router();
const fs = require('fs');
const uuidV4 = require('uuid/v4');

const Ocr = require('../controllers/ocr');
const bdImages = require('../models/images');
const { base64toBlob, base64toImage } = require('../utils/imagehandling');

// router.get('/extract/:id', async (req, res, next) => {

//     pyshell = await Ocr.extractInfoFromRaidImage(`${req.params.id}.jpg`)
//     await pyshell.on('message', (message) => {

//         extractedInfo = message;
//         console.log(message);

//         res.send(extractedInfo)
//     });

// })

router.post('/extract', async (req, res, next) => {

    // Read base64encode from request
    const base64Image = req.body.image.split(';base64,').pop();

    // Generate unique id
    const uuid = uuidV4();

    // Convert to .jpg datatype to extract raid information
    await base64toImage(base64Image, uuid);

    // Save image on database
    fs.readFile(`${uuid}.jpg`, (err, data) => {
        bdImages.create({ type: 'jpg', data: data.toString() })
    })

    // Execute python script to extract information
    pyshell = await Ocr.extractInfoFromRaidImage(`${uuid}.jpg`)

    await pyshell.on('message', (message) => {
        extractedInfo = message;
        console.log(message);
        res.send(extractedInfo)
    });

})


module.exports = router;

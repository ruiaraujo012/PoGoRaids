const express = require('express');
const router = express.Router();

const dbGym = require('../controllers/gym');

router.post('/create', async (req, res, next) => {

    const newGym = await dbGym.create(req.body);
    res.send(newGym.dataValues)

})

module.exports = router;

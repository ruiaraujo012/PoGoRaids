const Sequelize = require('sequelize');
const db = require('../database/db');


const Raid = db.sequelize.define('raid', {
    id: {
        type: Sequelize.INTEGER(11),
        allowNull: false,
        primaryKey: true,
        autoIncrement: true
    },
    level: {
        type: Sequelize.INTEGER(1)
    },
    pokemon: {
        type: Sequelize.STRING(50)
    },
    start_time: {
        type: Sequelize.DATE
    },
    extracted_phone_time: {
        type: Sequelize.DATE
    },
    extracted_raid_time: {
        type: Sequelize.DATE
    }
}, {
        tableName: 'raid'
    })


module.exports = Raid;
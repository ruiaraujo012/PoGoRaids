const Sequelize = require('sequelize');
const db = require('../database/db');

const Images = db.sequelize.define('images', {
    id: {
        type: Sequelize.INTEGER(11),
        allowNull: false,
        primaryKey: true,
        autoIncrement: true
    },
    type: {
        type: Sequelize.STRING,
    },
    data: {
        type: Sequelize.BLOB('long')
    }
}, {
        tableName: 'images'
    });


module.exports = Images;
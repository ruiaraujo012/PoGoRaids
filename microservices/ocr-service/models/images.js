const Sequelize = require('sequelize');
const db = require('../database/db');

const Images = db.sequelize.define('images', {
    oid: {
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
    // event_oid: {
    //   type: Sequelize.INTEGER(11),
    //   allowNull: true,
    //   references: {
    //     model: 'event',
    //     key: 'event_oid'
    //   }
}, {
        tableName: 'images'
    });


module.exports = Images;
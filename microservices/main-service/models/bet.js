const Sequelize = require('sequelize');
const db = require('../database/db');

const Bet = db.sequelize.define('bet', {
    oid: {
        type: Sequelize.INTEGER(11),
        allowNull: false,
        primaryKey: true,
        autoIncrement: true
    },
    wager: {
        type: Sequelize.DOUBLE,
        allowNull: false
    },
    userOid: {
        type: Sequelize.INTEGER(10),
        allowNull: false
    },
    eventOid: {
        type: Sequelize.INTEGER(11),
        allowNull: false
    }, result: {
        type: Sequelize.STRING(25)
    }, earnings: {
        type: Sequelize.DOUBLE
    }
    // event_oid: {
    //   type: Sequelize.INTEGER(11),
    //   allowNull: true,
    //   references: {
    //     model: 'event',
    //     key: 'event_oid'
    //   }
}, {
        tableName: 'bet'
    });


module.exports = Bet;